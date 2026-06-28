declare class bigint
    value: string
end



declare bigint: {
    --[[
        Creates a new bigint object for large integers.

        @param value string -- The bigint value.
        @return bigint -- The bigint object.
    ]]
    new: (value: string) -> bigint
}



declare class Model
    function get(self, key: string, value: any) -> Self
    function all(self) -> { Self }
    function filter(self, filterTable: { [string]: any }) -> { Self }
end



declare class Player extends Model
    discordId: number
    money: number
    extraData: { any }

    -- function isFriend(self, otherPlayer: Player): boolean
    -- function canAfford(self, amount: number): boolean
end

declare Player: Player



declare class Economy extends Model
    name: string
    icon: string
end

declare Economy: Economy



declare class Regime extends Model
    name: string
    background: string
end

declare Regime: Regime



declare class Ball extends Model
    country: string
    health: number
    attack: number
    rarity: number
    emojiId: number
    wildCard: string
    collectionCard: string
    credits: string
    capacityName: string
    capacityDescription: string
    capacityLogic: { any }
    enabled: boolean
    shortName: string?
    catchNames: { string }?
    tradeable: boolean
    economy: Economy?
    regime: Regime
end

declare Ball: Ball



declare class BallInstance extends Model -- TODO: Finish BallInstance type
    ball: Ball
    player: Player
end

declare BallInstance: BallInstance
