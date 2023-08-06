# Bovine

This package contains two essential parts of bovine. First
it defines `BovineActor`, which contains all the necessities
to write ActivityPub Clients. Furthermore, this package contains
the cryptographic routines to verify HTTP signatures.

Furthermore, the folder `examples` contains a few examples on
how `BovineActor` can be used. The cryptographic routines
are used in `bovine_fedi` to verify signatures.

Documentation is available at [ReadTheDocs](https://bovine.readthedocs.io/en/latest/)

## Example: Make a post aka Faking at being a Server

While [ActivityPub](https://www.w3.org/TR/activitypub/) specifies Server to Server and Client to Server, they really are just two sides of the same coin. In this example, we will work through how to use `BovineActor` to post a message.

Without having an ActivityPub Server supporting Client to Server, this will require a bit of setup. This setup will build a stub server that just allows other ActivityPub servers to associate us with a domain.

The stub server is given by the following snippet. One should note that it just answers with predefined json from a config file, that hasn't been generated yet. One could easily replace it with serving static files. See also [the Mastodon Blog](https://blog.joinmastodon.org/2018/06/how-to-implement-a-basic-activitypub-server/) for a similar implementation.

```python
import tomli
import json
from quart import Quart

app = Quart(__name__)

with open("server.toml", "rb") as fp:
    config = tomli.load(fp)

@app.get("/.well-known/webfinger")
async def webfinger():
    return json.loads(config["webfinger"])


@app.get("/actor")
async def actor():
    return json.loads(config["actor"])

if __name__ == "__main__":
    app.run()
```

The following script generates the config files. You will have to adapt the `hostname` variable and be able to serve the entire thing through https.

```python
import bovine
import tomli_w
import json

hostname = "bovine-demo.mymath.rocks"

public_key, private_key = bovine.utils.crypto.generate_public_private_key()
actor_url = f"https://{hostname}/actor"
actor = (
    bovine.activitystreams.build_actor("actor")
    .with_account_url(actor_url)
    .with_public_key(public_key)
)

webfinger = {
    "subject": f"acct:actor@{hostname}",
    "links": [
        {
            "href": actor_url,
            "rel": "self",
            "type": "application/activity+json",
        }
    ],
}

server_config = {"actor": json.dumps(actor.build()), "webfinger": json.dumps(webfinger)}

actor_config = {
    "account_url": actor_url,
    "public_key_url": f"{actor_url}#main-key",
    "private_key": private_key,
}

with open("server.toml", "wb") as fp:
    tomli_w.dump(server_config, fp)

with open("bovine.toml", "wb") as fp:
    tomli_w.dump(actor_config, fp)
```

You can now access the urls, which are in my case [https://bovine-demo.mymath.rocks/actor](https://bovine-demo.mymath.rocks/actor) and [https://bovine-demo.mymath.rocks/.well-known/webfinger?resource=acct:actor@bovine-demo.mymath.rocks](https://bovine-demo.mymath.rocks/.well-known/webfinger?resource=acct:actor@bovine-demo.mymath.rocks). Using this, we can now lookup the fediverse handle `actor@bovine-demo.mymath.rocks` on most FediVerse applications.

You can now send a post via the following code snippet:

```python
import asyncio

from uuid import uuid4
from bovine import BovineActor

target_account = "https://mas.to/users/themilkman"


async def run():
    async with BovineActor.from_file("bovine.toml") as actor:
        activity_factory, object_factory = actor.factories
        note = (
            object_factory.note("Hello")
            .add_to(target_account)
            .with_mention(target_account)
            .build()
        )
        note["id"] = actor.actor_id + "/" + str(uuid4())
        create = activity_factory.create(note).build()
        create["id"] = actor.actor_id + "/" + str(uuid4())

        remote_actor = await actor.get(target_account)
        target_inbox = remote_actor["inbox"]
        await actor.post(target_inbox, create)


asyncio.run(run())
```

A few comments are in order:

- The id needs to be set on the Note and Create in order to be compatible with Mastodon. When using proper Client To Server as below, it is superfluous
- The form of adding the `target_account` to both to and mention causes it to be a direct message.

## Using BovineClient

One can import it via `from bovine import BovineClient`. Then one can either use it via:

```python
async with BovineClient(config) as actor:
    ...
# or
actor = BovineClient(config)
await actor.init()
```

Here the config object can be present in two variants. First it can contain the keys `host` and `private_key`, where `host` is the domain the ActivityPub Actor is on and `private_key` is a mutlicodec encoded Ed25519 key, whose corresponding did-key has been added to the Actor. In this case [Moo-Auth-1](https://blog.mymath.rocks/2023-03-15/BIN1_Moo_Authentication_and_Authoriation) will be used. The second variant is to use [HTTP Signatures](https://docs.joinmastodon.org/spec/security/#http), where the keys `account_url`, `public_key_url`, and `private_key` need to be present. Alternatively, to passing a config object, one can use `BovineActor.from_file(path_to_toml_file)`.

### Making a post

BovineActor contains two factories to create [ActivityStreams Objects](https://www.w3.org/TR/activitystreams-vocabulary/#object-types) and [ActivityStreams Activities](https://www.w3.org/TR/activitystreams-vocabulary/#activity-types). One can obtain them by running

```python
activity_factory, object_factory = actor.factories
```

The simplest usage example is a create wrapping a note, that looks like:

```python
activity_factory, object_factory = actor.factories
note = object_factory.note("Hello").as_public().build()
create = activity_factory.create(note).build()
```

The result should be the something equivalent to the json

```json
{
  "@context": "https://www.w3.org/ns/activitystreams",
  "type": "Create",
  "actor": "https://domain/actor",
  "object": {
    "attributedTo": "https://domain/actor",
    "type": "Note",
    "content": "Hello",
    "published": "2023-03-25T08:12:32Z",
    "to": "as:Public",
    "cc": "https://domain/followers_collection"
  },
  "published": "2023-03-25T08:12:32Z",
  "to": "as:Public",
  "cc": "https://domain/followers_collection"
}
```

The details depend on the used actor and will likely contain superfluous elements until the creation process is improved. We can now send this activity to our outbox using

```python
await actor.send_to_outbox(create)
```

__Note__: This is different from what we did in the first example, where we used `await actor.post(inbox, create)`. The difference is that in the first example, we faked being a server, now we are actually using Client To Server.

### The inbox and outbox

By running

```python
inbox = await actor.inbox()
outbox = await actor.outbox()
```

one can obtain `CollectionHelper` objects. These are meant to make it easier to interact with collection objects. In the simplest use case, one can use

```python
await inbox.next_item()
```

to get the items from the inbox one after the other. It is also possible to print a summary of all elements that have been fetched from the inbox using `await inbox.summary()`. Finally, it is possible to iterate over the inbox via

```python
async for item in inbox.iterate(max_number=3):
    do_something(item)
```

### Proxying elements

We have already seen the difference between using `post` directly to an inbox and posting to the actor's outbox using `send_to_outbox`. A similar pattern applies to fetching objects. Both of these commands often have a similar result

```python
await actor.get(object_id)
await actor.proxy_element(object_id)
```

However, they do different things:

- The first `actor.get` sends a webrequest to the server `object_id` is on and retrieves it
- The second `actor.proxy_element` sends a request to the actor's server for the object. This request is then either answered from the server's object store or by the server fetching the object. The cache behavior is up to the server. Depending of the evolution of `proxyUrl` of an Actor, more options might be added here.

As most servers don't support Moo-Auth-1, using `proxy_element` is the only way to obtain foreign objects, when using it.

### Event Source

The event source is demonstrated in `examples/sse.py`. First, the event source will be specified in a [FEP](https://codeberg.org/fediverse/fep) to come. It provides a way to receive updates from the server, whenever a new element is added to the inbox or outbox. The basic usage is

```python
event_source = await actor.event_source()
async for event in event_source:
    if event and event.data:
        data = json.loads(event.data)
        do_something(data)
```

If you plan on writing long running applications, the event source does not automatically reconnect, so you will need to implement this. [mechanical_bull](https://codeberg.org/helge/mechanical_bull) uses the event source in this way.
