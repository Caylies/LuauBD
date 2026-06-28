# LuauBD

A Luau runtime for the Ballsdex Discord bot.

```luau
local ball = Ball.get("country", "British Empire")
print(ball.country) -- British Empire
```

## Installation

The LuauBD package needs additional dependencies to work. In `Dockerfile`, make the following changes:

```diff
-RUN apk add --no-cache gcc libc-dev git
+RUN apk add --no-cache gcc libc-dev git g++ musl-dev
```

## Runtime Globals

### `bigint` (class)

```luau
Player.get("discord_id", bigint.new("999736048596816014"))
```

The `bigint` class allows you to hold integers that exceed Luau's integer limit. The bigint class should be used for storing large integers such as Discord IDs.

- `bigint.new(value: string): bigint` - Creates a new bigint object.
