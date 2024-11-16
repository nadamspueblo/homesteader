enum ActionKind {
    Walking,
    Idle,
    Jumping,
    WalkRight,
    WalkDown,
    WalkLeft,
    WalkUp,
    SwingAxRight,
    SwingAxLeft,
    SwingAxDown,
    SwingAxUp
}
namespace SpriteKind {
    export const Menu = SpriteKind.create()
    export const npc = SpriteKind.create()
    export const coin = SpriteKind.create()
    export const structure = SpriteKind.create()
}
function useShovel () {
    prepareGround()
}
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function (sprite, otherSprite) {
    if (controller.A.isPressed()) {
        sprites.destroy(otherSprite, effects.disintegrate, 500)
        activeTool = "ax"
        info.changeScoreBy(10)
        savePlayerInfo()
    } else {
        scene.cameraShake(4, 500)
        otherSprite.x += 32
        otherSprite.y += 32
        info.changeLifeBy(-1)
        savePlayerInfo()
    }
})
function showSupplyMenu () {
    controller.moveSprite(playerSprite, 0, 0)
    supplyMenuSprites = []
    prevX = scene.cameraProperty(CameraProperty.X)
    for (let index = 0; index <= supplyInventory.length - 1; index++) {
        textSprite = textsprite.create("" + supplyInvCount[index], 1, 15)
        textSprite.setIcon(supplyIcons[supplyIndex.indexOf(supplyInventory[index])])
        if (supplyInventory[index] == activeSupply) {
            textSprite.setBorder(1, 5)
        } else {
            textSprite.setBorder(1, 1)
        }
        textSprite.setPosition(prevX, scene.cameraProperty(CameraProperty.Bottom) - 24)
        prevX = prevX + textSprite.width
        supplyMenuSprites.push(textSprite)
    }
}
function playBeginning () {
    if (gameStepCount == 20) {
        playerSprite.sayText("I can't believe the deal I got on this land", 5000, true)
    } else if (gameStepCount == 110) {
        playerSprite.sayText("I should plant the last of my food.", 5000, true)
    } else if (gameStepCount == 160) {
        playerSprite.sayText("I can sell what I grow in town", 5000, true)
    } else {
    	
    }
}
function isInFarm () {
    return playerSprite.tilemapLocation().column < 39 && playerSprite.tilemapLocation().column > 12 && (playerSprite.tilemapLocation().row < 93 && playerSprite.tilemapLocation().row > 73)
}
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile4`, function (sprite, location) {
    tiles.placeOnTile(helperSprite, location)
    helperSprite.sayText("" + Math.idiv(locationTimers[timedLocations.indexOf(location.column * 100 + location.row)] - gameStepCount, 10) + "s", 1000, false)
})
controller.up.onEvent(ControllerButtonEvent.Pressed, function () {
    if (controller.A.isPressed() && activeTool == "shovel") {
    	
    } else if (!(controller.B.isPressed())) {
        if (!(controller.left.isPressed() || controller.right.isPressed())) {
            animation.setAction(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        }
    } else {
    	
    }
})
function prepareGround () {
    if (playerSprite.tilemapLocation().column < 39 && playerSprite.tilemapLocation().column > 12) {
        if (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), sprites.castle.tileGrass1) || (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), sprites.castle.tileGrass3) || tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), sprites.castle.tilePath5))) {
            modifiedLocations.push(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)
            locationTypes.push(tileIndex.indexOf(assets.tile`myTile`))
            tiles.setTileAt(playerSprite.tilemapLocation(), assets.tile`myTile`)
            saveGame()
        } else if (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile20`) || tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile2`)) {
            modifiedLocations.push(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)
            locationTypes.push(tileIndex.indexOf(sprites.castle.tileGrass1))
            tiles.setTileAt(playerSprite.tilemapLocation(), sprites.castle.tileGrass1)
            saveGame()
        } else if (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile21`)) {
            modifiedLocations.push(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)
            locationTypes.push(tileIndex.indexOf(sprites.castle.tilePath5))
            blockSettings.writeString("snake grass shovel tip", "true")
            tiles.setTileAt(playerSprite.tilemapLocation(), sprites.castle.tilePath5)
            saveGame()
        } else {
        	
        }
    }
}
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (false) {
    	
    } else if (activeTool == "ax") {
        if (playerFacing == "right") {
            animation.setAction(playerSprite, ActionKind.SwingAxRight)
        } else if (playerFacing == "left") {
            animation.setAction(playerSprite, ActionKind.SwingAxLeft)
        } else if (playerFacing == "down") {
            animation.setAction(playerSprite, ActionKind.SwingAxDown)
        } else {
            animation.setAction(playerSprite, ActionKind.SwingAxUp)
        }
        chopTrees()
    } else if (activeTool == "pick") {
        usePick()
    } else if (isInFarm()) {
        if (activeTool == "shovel") {
            if (playerSprite.tileKindAt(TileDirection.Center, assets.tile`myTile`)) {
                showSupplyMenu()
            }
        } else if (activeTool == "hammer") {
            if (playerSprite.tileKindAt(TileDirection.Center, assets.tile`myTile`)) {
                showSupplyMenu()
            }
        }
    }
})
controller.left.onEvent(ControllerButtonEvent.Released, function () {
    if (!(controller.B.isPressed())) {
        if (controller.up.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        } else if (controller.down.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        } else if (controller.right.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
        }
    }
})
controller.B.onEvent(ControllerButtonEvent.Released, function () {
    controller.moveSprite(playerSprite, 50, 50)
    hideToolMenu()
    savePlayerInfo()
})
controller.A.onEvent(ControllerButtonEvent.Released, function () {
    hideSupplyMenu()
    if (playerSprite.tileKindAt(TileDirection.Center, assets.tile`myTile5`)) {
        harvestCarrot()
    } else if (activeTool == "shovel" && isInFarm()) {
        if (playerSprite.tileKindAt(TileDirection.Center, assets.tile`myTile`)) {
            plantFood()
        } else {
            useShovel()
        }
    }
})
function hideSupplyMenu () {
    controller.moveSprite(playerSprite, 50, 50)
    for (let value of supplyMenuSprites) {
        sprites.destroy(value)
    }
    supplyMenuSprites = []
}
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile11`, function (sprite, location) {
    if (!(shopIsOpen)) {
        farmer.sayText("Carrots for sale (A)", 100, false)
        if (controller.A.isPressed()) {
            shopIsOpen = true
            tiles.placeOnTile(playerSprite, tiles.getTileLocation(location.column, location.row + 2))
            answer = game.askForNumber("How many would you like to buy? ($3 each)")
            if (answer > 0) {
                if (3 * answer <= cashMoney) {
                    cashMoney = cashMoney - 3 * answer
                    supplyInvCount[0] = supplyInvCount[0] + answer
                    if (!(blockSettings.exists("hasBoughtFood"))) {
                        blockSettings.writeString("hasBoughtFood", "true")
                    }
                    saveInventory()
                    farmer.sayText("Thank you, Have a nice day!", 2000, false)
                } else {
                    farmer.sayText("You don't have enough money", 2000, false)
                }
            } else {
                farmer.sayText("Have a nice day!", 2000, false)
            }
            shopIsOpen = false
        }
    } else {
        tiles.placeOnTile(playerSprite, tiles.getTileLocation(location.column, location.row + 2))
    }
})
function build () {
    if (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile`)) {
        tiles.setTileAt(playerSprite.tilemapLocation(), assets.tile`myTile3`)
        tiles.setWallAt(playerSprite.tilemapLocation(), true)
        modifiedLocations.push(col * 100 + row)
        locationTypes.push(3)
        saveGame()
    }
}
controller.right.onEvent(ControllerButtonEvent.Released, function () {
    if (!(controller.B.isPressed())) {
        if (controller.up.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        } else if (controller.down.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        } else if (controller.left.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
        }
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile21`, function (sprite, location) {
    if (hasTimerEnded("bushTriggerDelay")) {
        if (Math.percentChance(25) && enemyList.length < maxEnemies) {
            snake = sprites.create(img`
                . . . . c c c c c c . . . . . . 
                . . . c 6 7 7 7 7 6 c . . . . . 
                . . c 7 7 7 7 7 7 7 7 c . . . . 
                . c 6 7 7 7 7 7 7 7 7 6 c . . . 
                . c 7 c 6 6 6 6 c 7 7 7 c . . . 
                . f 7 6 f 6 6 f 6 7 7 7 f . . . 
                . f 7 7 7 7 7 7 7 7 7 7 f . . . 
                . . f 7 7 7 7 6 c 7 7 6 f c . . 
                . . . f c c c c 7 7 6 f 7 7 c . 
                . . c 7 2 7 7 7 6 c f 7 7 7 7 c 
                . c 7 7 2 7 7 c f c 6 7 7 6 c c 
                c 1 1 1 1 7 6 f c c 6 6 6 c . . 
                f 1 1 1 1 1 6 6 c 6 6 6 6 f . . 
                f 6 1 1 1 1 1 6 6 6 6 6 c f . . 
                . f 6 1 1 1 1 1 1 6 6 6 f . . . 
                . . c c c c c c c c c f . . . . 
                `, SpriteKind.Enemy)
            snake.setPosition(playerSprite.x + 24, playerSprite.y + 24)
            animation.runImageAnimation(
            snake,
            [img`
                . . . . c c c c c c . . . . . . 
                . . . c 6 7 7 7 7 6 c . . . . . 
                . . c 7 7 7 7 7 7 7 7 c . . . . 
                . c 6 7 7 7 7 7 7 7 7 6 c . . . 
                . c 7 c 6 6 6 6 c 7 7 7 c . . . 
                . f 7 6 f 6 6 f 6 7 7 7 f . . . 
                . f 7 7 7 7 7 7 7 7 7 7 f . . . 
                . . f 7 7 7 7 6 c 7 7 6 f c . . 
                . . . f c c c c 7 7 6 f 7 7 c . 
                . . c 7 2 7 7 7 6 c f 7 7 7 7 c 
                . c 7 7 2 7 7 c f c 6 7 7 6 c c 
                c 1 1 1 1 7 6 f c c 6 6 6 c . . 
                f 1 1 1 1 1 6 6 c 6 6 6 6 f . . 
                f 6 1 1 1 1 1 6 6 6 6 6 c f . . 
                . f 6 1 1 1 1 1 1 6 6 6 f . . . 
                . . c c c c c c c c c f . . . . 
                `,img`
                . . . c c c c c c . . . . . . . 
                . . c 6 7 7 7 7 6 c . . . . . . 
                . c 7 7 7 7 7 7 7 7 c . . . . . 
                c 6 7 7 7 7 7 7 7 7 6 c . . . . 
                c 7 c 6 6 6 6 c 7 7 7 c . . . . 
                f 7 6 f 6 6 f 6 7 7 7 f . . . . 
                f 7 7 7 7 7 7 7 7 7 7 f . . . . 
                . f 7 7 7 7 6 c 7 7 6 f . . . . 
                . . f c c c c 7 7 6 f c c c . . 
                . . c 6 2 7 7 7 f c c 7 7 7 c . 
                . c 6 7 7 2 7 7 c f 6 7 7 7 7 c 
                . c 1 1 1 1 7 6 6 c 6 6 6 c c c 
                . c 1 1 1 1 1 6 6 6 6 6 6 c . . 
                . c 6 1 1 1 1 1 6 6 6 6 6 c . . 
                . . c 6 1 1 1 1 1 7 6 6 c c . . 
                . . . c c c c c c c c c c . . . 
                `],
            200,
            true
            )
            animation.runMovementAnimation(
            snake,
            animation.animationPresets(animation.shake),
            200,
            false
            )
            snake.follow(playerSprite, 10)
            enemyList.push(snake)
            if (!(blockSettings.exists("snake warning"))) {
                blockSettings.writeString("snake warning", "true")
                playerSprite.sayText("A snake ... run!!", 2000, false)
            } else if (false) {
            	
            } else if (toolInventory.indexOf("ax") >= 0 && blockSettings.exists("kill snake ax")) {
                playerSprite.sayText("I could kill it with my ax", 2000, false)
                blockSettings.writeNumber("kill snake ax", 1)
            } else {
            	
            }
        } else if (isInFarm() && !(blockSettings.exists("snake grass shovel tip"))) {
            playerSprite.sayText("I should dig up that snake den", 2000, false)
        } else if (!(isInFarm()) && !(blockSettings.exists("avoid snake grass tip"))) {
            blockSettings.writeString("avoid snake grass tip", "true")
            playerSprite.sayText("I should watch out for snake dens", 2000, false)
        } else {
        	
        }
    }
    setEventTimer("bushTriggerDelay", 20)
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile12`, function (sprite, location) {
    if (!(shopIsOpen)) {
        farmer.sayText("Want to sell some food? (A)", 100, false)
        if (controller.A.isPressed()) {
            shopIsOpen = true
            tiles.placeOnTile(playerSprite, tiles.getTileLocation(location.column, location.row + 2))
            answer = game.askForNumber("How many would you like to sell? ($2 each)")
            if (answer > 0) {
                if (answer <= supplyInvCount[0]) {
                    cashMoney = cashMoney + answer * 2
                    supplyInvCount[0] = supplyInvCount[0] - answer
                    saveInventory()
                    farmer.sayText("Thank you, Have a nice day!", 2000, false)
                } else {
                    farmer.sayText("You don't have enough inventory", 2000, false)
                }
            } else {
                farmer.sayText("Have a nice day!", 2000, false)
            }
            shopIsOpen = false
        }
    }
})
function loadSave () {
    if (blockSettings.exists("timedLocations")) {
        timedLocations = blockSettings.readNumberArray("timedLocations")
        timedTypes = blockSettings.readNumberArray("timedTypes")
        locationTimers = blockSettings.readNumberArray("locationTimers")
        for (let index = 0; index <= timedLocations.length; index++) {
            col = Math.idiv(timedLocations[index], 100)
            row = timedLocations[index] % 100
            if (timedTypes[index] == 2) {
                tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile2`)
                tiles.setWallAt(tiles.getTileLocation(col, row), false)
            } else if (timedTypes[index] == 4) {
                tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile4`)
            }
        }
    }
    if (blockSettings.exists("modifiedLocations")) {
        modifiedLocations = blockSettings.readNumberArray("modifiedLocations")
        locationTypes = blockSettings.readNumberArray("locationTypes")
        for (let index = 0; index <= modifiedLocations.length; index++) {
            col = Math.idiv(modifiedLocations[index], 100)
            row = modifiedLocations[index] % 100
            if (locationTypes[index] == 1) {
                tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile`)
            } else if (locationTypes[index] == 3) {
                tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile3`)
                tiles.setWallAt(tiles.getTileLocation(col, row), true)
            } else if (locationTypes[index] == 5) {
                tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile5`)
            } else if (locationTypes[index] == 0) {
                tiles.setTileAt(tiles.getTileLocation(col, row), sprites.castle.tileGrass1)
            } else {
            	
            }
        }
    }
    if (blockSettings.exists("gameStepCount")) {
        gameStepCount = blockSettings.readNumber("gameStepCount")
    }
    if (blockSettings.exists("wood")) {
        wood = blockSettings.readNumber("wood")
    }
    if (blockSettings.exists("foodInventory")) {
        supplyInvCount = blockSettings.readNumberArray("foodInventory")
    }
    if (blockSettings.exists("playerX")) {
        playerSprite.x = blockSettings.readNumber("playerX")
        playerSprite.y = blockSettings.readNumber("playerY")
    }
    if (blockSettings.exists("cashMoney")) {
        cashMoney = blockSettings.readNumber("cashMoney")
    }
    if (blockSettings.exists("score")) {
        info.setScore(blockSettings.readNumber("score"))
    }
    if (blockSettings.exists("activeTool")) {
        activeTool = blockSettings.readString("activeTool")
        toolSprite.setImage(toolIcons[toolIndex.indexOf(activeTool)])
    }
}
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile18`, function (sprite, location) {
    if (!(shopIsOpen)) {
        blacksmith.sayText("Need a pick? (A)", 100, false)
        if (controller.A.isPressed()) {
            shopIsOpen = true
            tiles.placeOnTile(playerSprite, tiles.getTileLocation(location.column + 2, location.row))
            yesnoAnswer = game.ask("That will be $250")
            if (yesnoAnswer) {
                if (250 <= cashMoney) {
                    cashMoney = cashMoney - 250
                    toolInventory.push("pick")
                    saveInventory()
                    farmer.sayText("Thank you, Have a nice day!", 2000, false)
                } else {
                    farmer.sayText("You don't have enough money", 2000, false)
                }
            } else {
                farmer.sayText("Have a nice day!", 2000, false)
            }
            shopIsOpen = false
        }
    } else {
        tiles.placeOnTile(playerSprite, tiles.getTileLocation(location.column + 2, location.row))
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile5`, function (sprite, location) {
    tiles.placeOnTile(helperSprite, location)
    helperSprite.sayText("Harvest (A)", 100, false)
})
function initGameData () {
    info.setLife(2)
    activeTool = "hand"
    toolInventory = ["hand", "shovel"]
    toolIndex = [
    "ax",
    "hammer",
    "shovel",
    "pick",
    "hand"
    ]
    toolIcons = [
    assets.image`ax icon inactive`,
    assets.image`hammer icon inactive`,
    assets.image`shovel icon inactive`,
    assets.image`pick icon inactive`,
    assets.image`hand icon inactive`
    ]
    activeToolIcons = [
    assets.image`ax icon active`,
    assets.image`hammer icon active`,
    assets.image`shovel icon active`,
    assets.image`pick icon active`,
    assets.image`hand icon active`
    ]
    wood = 0
    supplyInvCount = [1, 0]
    supplyInventory = ["carrot", "wood"]
    supplyIndex = ["carrot", "wood", "stone"]
    supplyIcons = [assets.image`carrot icon`, assets.image`wood icon`, assets.image`stone icon`]
    activeSupply = "carrot"
    gameStepCount = 0
    timedLocations = []
    locationTimers = []
    timedTypes = []
    modifiedLocations = []
    locationTypes = []
    shopIsOpen = false
    cashMoney = 5
    info.setScore(0)
    maxEnemies = 1
    enemyList = []
    eventTimers = []
    eventTimerNames = []
    tileIndex = [
    assets.tile`myTile5`,
    assets.tile`myTile4`,
    assets.tile`myTile`,
    assets.tile`myTile21`,
    sprites.castle.tileGrass1,
    sprites.castle.tileGrass3,
    sprites.castle.tilePath5,
    assets.tile`myTile27`,
    assets.tile`myTile22`
    ]
}
function showToolMenu () {
    menuSprites = []
    for (let index = 0; index <= toolInventory.length - 1; index++) {
        if (toolInventory[index] == activeTool) {
            menuSprite = sprites.create(activeToolIcons[toolIndex.indexOf(toolInventory[index])], SpriteKind.Menu)
            menuSprite.setPosition(scene.cameraProperty(CameraProperty.X) + index * 16, scene.cameraProperty(CameraProperty.Bottom) - 24)
            menuSprites.push(menuSprite)
        } else {
            menuSprite = sprites.create(toolIcons[toolIndex.indexOf(toolInventory[index])], SpriteKind.Menu)
            menuSprite.setPosition(scene.cameraProperty(CameraProperty.X) + index * 16, scene.cameraProperty(CameraProperty.Bottom) - 24)
            menuSprites.push(menuSprite)
        }
    }
    textSprites = []
    infoBgSprite = sprites.create(img`
        ..8888888888888888888888888888888888888888888888888888..
        .811111111111111111111111111111111111111111111111111118.
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        81111111111111111111111111111111111111111111111111111118
        .811111111111111111111111111111111111111111111111111118.
        ..8888888888888888888888888888888888888888888888888888..
        `, SpriteKind.Text)
    infoBgSprite.setPosition(scene.cameraProperty(CameraProperty.Right) - infoBgSprite.width / 2, scene.cameraProperty(CameraProperty.Top) + infoBgSprite.height)
    textSprite = textsprite.create("x" + cashMoney, 1, 15)
    textSprite.setIcon(img`
        . . . b b . . . 
        . . b 5 5 b . . 
        . b 5 d 1 5 b . 
        . b 5 3 1 5 b . 
        . c 5 3 1 d c . 
        . c 5 1 d d c . 
        . . f d d f . . 
        . . . f f . . . 
        `)
    textSprite.setPosition(scene.cameraProperty(CameraProperty.Right) - (textSprite.width / 2 + 4), scene.cameraProperty(CameraProperty.Top) + 32)
    textSprites.push(textSprite)
    textSprite = textsprite.create("x" + supplyInvCount[0], 1, 15)
    textSprite.setIcon(assets.image`carrot icon`)
    textSprite.setPosition(scene.cameraProperty(CameraProperty.Right) - (textSprite.width / 2 + 4), scene.cameraProperty(CameraProperty.Top) + 42)
    textSprites.push(textSprite)
}
function setupCharacterAnim () {
    anim = animation.createAnimation(ActionKind.WalkDown, 200)
    anim.addAnimationFrame(img`
        . . . . . . f f f f . . . . . . 
        . . . . f f f 2 2 f f f . . . . 
        . . . f f f 2 2 2 2 f f f . . . 
        . . f f f e e e e e e f f f . . 
        . . f f e 2 2 2 2 2 2 e e f . . 
        . . f e 2 f f f f f f 2 e f . . 
        . . f f f f e e e e f f f f . . 
        . f f e f b f 4 4 f b f e f f . 
        . f e e 4 1 f d d f 1 4 e e f . 
        . . f e e d d d d d d e e f . . 
        . . . f e e 4 4 4 4 e e f . . . 
        . . e 4 f 2 2 2 2 2 2 f 4 e . . 
        . . 4 d f 2 2 2 2 2 2 f d 4 . . 
        . . 4 4 f 4 4 5 5 4 4 f 4 4 . . 
        . . . . . f f f f f f . . . . . 
        . . . . . f f . . f f . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . . . f f f f . . . . . . 
        . . . . f f f 2 2 f f f . . . . 
        . . . f f f 2 2 2 2 f f f . . . 
        . . f f f e e e e e e f f f . . 
        . . f f e 2 2 2 2 2 2 e e f . . 
        . f f e 2 f f f f f f 2 e f f . 
        . f f f f f e e e e f f f f f . 
        . . f e f b f 4 4 f b f e f . . 
        . . f e 4 1 f d d f 1 4 e f . . 
        . . . f e 4 d d d d 4 e f e . . 
        . . f e f 2 2 2 2 e d d 4 e . . 
        . . e 4 f 2 2 2 2 e d d e . . . 
        . . . . f 4 4 5 5 f e e . . . . 
        . . . . f f f f f f f . . . . . 
        . . . . f f f . . . . . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . f f f f . . . . . . 
        . . . . f f f 2 2 f f f . . . . 
        . . . f f f 2 2 2 2 f f f . . . 
        . . f f f e e e e e e f f f . . 
        . . f f e 2 2 2 2 2 2 e e f . . 
        . . f e 2 f f f f f f 2 e f . . 
        . . f f f f e e e e f f f f . . 
        . f f e f b f 4 4 f b f e f f . 
        . f e e 4 1 f d d f 1 4 e e f . 
        . . f e e d d d d d d e e f . . 
        . . . f e e 4 4 4 4 e e f . . . 
        . . e 4 f 2 2 2 2 2 2 f 4 e . . 
        . . 4 d f 2 2 2 2 2 2 f d 4 . . 
        . . 4 4 f 4 4 5 5 4 4 f 4 4 . . 
        . . . . . f f f f f f . . . . . 
        . . . . . f f . . f f . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . . . f f f f . . . . . . 
        . . . . f f f 2 2 f f f . . . . 
        . . . f f f 2 2 2 2 f f f . . . 
        . . f f f e e e e e e f f f . . 
        . . f e e 2 2 2 2 2 2 e f f . . 
        . f f e 2 f f f f f f 2 e f f . 
        . f f f f f e e e e f f f f f . 
        . . f e f b f 4 4 f b f e f . . 
        . . f e 4 1 f d d f 1 4 e f . . 
        . . e f e 4 d d d d 4 e f . . . 
        . . e 4 d d e 2 2 2 2 f e f . . 
        . . . e d d e 2 2 2 2 f 4 e . . 
        . . . . e e f 5 5 4 4 f . . . . 
        . . . . . f f f f f f f . . . . 
        . . . . . . . . . f f f . . . . 
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.WalkRight, 200)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . . f f f f f f . . . . . 
        . . . f f e e e e f 2 f . . . . 
        . . f f e e e e f 2 2 2 f . . . 
        . . f e e e f f e e e e f . . . 
        . . f f f f e e 2 2 2 2 e f . . 
        . . f e 2 2 2 f f f f e 2 f . . 
        . f f f f f f f e e e f f f . . 
        . f f e 4 4 e b f 4 4 e e f . . 
        . f e e 4 d 4 1 f d d e f . . . 
        . . f e e e e e d d d f . . . . 
        . . . . f 4 d d e 4 e f . . . . 
        . . . . f e d d e 2 2 f . . . . 
        . . . f f f e e f 5 5 f f . . . 
        . . . f f f f f f f f f f . . . 
        . . . . f f . . . f f f . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . f f f f f f . . . . 
        . . . . f f e e e e f 2 f . . . 
        . . . f f e e e e f 2 2 2 f . . 
        . . . f e e e f f e e e e f . . 
        . . . f f f f e e 2 2 2 2 e f . 
        . . . f e 2 2 2 f f f f e 2 f . 
        . . f f f f f f f e e e f f f . 
        . . f f e 4 4 e b f 4 4 e e f . 
        . . f e e 4 d 4 1 f d d e f . . 
        . . . f e e e 4 d d d d f . . . 
        . . . . f f e e 4 4 4 e f . . . 
        . . . . . 4 d d e 2 2 2 f . . . 
        . . . . . e d d e 2 2 2 f . . . 
        . . . . . f e e f 4 5 5 f . . . 
        . . . . . . f f f f f f . . . . 
        . . . . . . . f f f . . . . . . 
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.WalkLeft, 200)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . f f f f f f . . . . . . 
        . . . f 2 f e e e e f f . . . . 
        . . f 2 2 2 f e e e e f f . . . 
        . . f e e e e f f e e e f . . . 
        . f e 2 2 2 2 e e f f f f . . . 
        . f 2 e f f f f 2 2 2 e f . . . 
        . f f f e e e f f f f f f f . . 
        . f e e 4 4 f b e 4 4 e f f . . 
        . . f e d d f 1 4 d 4 e e f . . 
        . . . f d d d e e e e e f . . . 
        . . . f e 4 e d d 4 f . . . . . 
        . . . f 2 2 e d d e f . . . . . 
        . . f f 5 5 f e e f f f . . . . 
        . . f f f f f f f f f f . . . . 
        . . . f f f . . . f f . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . f f f f f f . . . . . . 
        . . . f 2 f e e e e f f . . . . 
        . . f 2 2 2 f e e e e f f . . . 
        . . f e e e e f f e e e f . . . 
        . f e 2 2 2 2 e e f f f f . . . 
        . f 2 e f f f f 2 2 2 e f . . . 
        . f f f e e e f f f f f f f . . 
        . f e e 4 4 f b e 4 4 e f f . . 
        . . f e d d f 1 4 d 4 e e f . . 
        . . . f d d d d 4 e e e f . . . 
        . . . f e 4 4 4 e e f f . . . . 
        . . . f 2 2 2 e d d 4 . . . . . 
        . . . f 2 2 2 e d d e . . . . . 
        . . . f 5 5 4 f e e f . . . . . 
        . . . . f f f f f f . . . . . . 
        . . . . . . f f f . . . . . . . 
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.WalkUp, 200)
    anim.addAnimationFrame(img`
        . . . . . . f f f f . . . . . . 
        . . . . f f e e e e f f . . . . 
        . . . f e e e f f e e e f . . . 
        . . f f f f f 2 2 f f f f f . . 
        . . f f e 2 e 2 2 e 2 e f f . . 
        . . f e 2 f 2 f f 2 f 2 e f . . 
        . . f f f 2 2 e e 2 2 f f f . . 
        . f f e f 2 f e e f 2 f e f f . 
        . f e e f f e e e e f e e e f . 
        . . f e e e e e e e e e e f . . 
        . . . f e e e e e e e e f . . . 
        . . e 4 f f f f f f f f 4 e . . 
        . . 4 d f 2 2 2 2 2 2 f d 4 . . 
        . . 4 4 f 4 4 4 4 4 4 f 4 4 . . 
        . . . . . f f f f f f . . . . . 
        . . . . . f f . . f f . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . . . f f f f . . . . . . 
        . . . . f f e e e e f f . . . . 
        . . . f e e e f f e e e f . . . 
        . . . f f f f 2 2 f f f f . . . 
        . . f f e 2 e 2 2 e 2 e f f . . 
        . . f e 2 f 2 f f f 2 f e f . . 
        . . f f f 2 f e e 2 2 f f f . . 
        . . f e 2 f f e e 2 f e e f . . 
        . f f e f f e e e f e e e f f . 
        . f f e e e e e e e e e e f f . 
        . . . f e e e e e e e e f . . . 
        . . . e f f f f f f f f 4 e . . 
        . . . 4 f 2 2 2 2 2 e d d 4 . . 
        . . . e f f f f f f e e 4 . . . 
        . . . . f f f . . . . . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . f f f f . . . . . . 
        . . . . f f e e e e f f . . . . 
        . . . f e e e f f e e e f . . . 
        . . f f f f f 2 2 f f f f f . . 
        . . f f e 2 e 2 2 e 2 e f f . . 
        . . f e 2 f 2 f f 2 f 2 e f . . 
        . . f f f 2 2 e e 2 2 f f f . . 
        . f f e f 2 f e e f 2 f e f f . 
        . f e e f f e e e e f e e e f . 
        . . f e e e e e e e e e e f . . 
        . . . f e e e e e e e e f . . . 
        . . e 4 f f f f f f f f 4 e . . 
        . . 4 d f 2 2 2 2 2 2 f d 4 . . 
        . . 4 4 f 4 4 4 4 4 4 f 4 4 . . 
        . . . . . f f f f f f . . . . . 
        . . . . . f f . . f f . . . . . 
        `)
    anim.addAnimationFrame(img`
        . . . . . . . . . . . . . . . . 
        . . . . . . f f f f . . . . . . 
        . . . . f f e e e e f f . . . . 
        . . . f e e e f f e e e f . . . 
        . . . f f f f 2 2 f f f f . . . 
        . . f f e 2 e 2 2 e 2 e f f . . 
        . . f e f 2 f f f 2 f 2 e f . . 
        . . f f f 2 2 e e f 2 f f f . . 
        . . f e e f 2 e e f f 2 e f . . 
        . f f e e e f e e e f f e f f . 
        . f f e e e e e e e e e e f f . 
        . . . f e e e e e e e e f . . . 
        . . e 4 f f f f f f f f e . . . 
        . . 4 d d e 2 2 2 2 2 f 4 . . . 
        . . . 4 e e f f f f f f e . . . 
        . . . . . . . . . f f f . . . . 
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.SwingAxRight, 100)
    anim.addAnimationFrame(img`
        .....fff.............
        ....fff2ff...........
        ..ffeeef2ff..........
        .ffeeeef2eff.........
        .feeeeffeeeef....fff.
        .fffffe22222f...fccf.
        .ffe222ffff2f..fccbf.
        ffffffffeeeff.feccbf.
        fefe441ff4eeffeecbf..
        ffee4d4bdddeffeeff...
        .ffeee4dddeedeef.....
        ..ff2222eeddeef......
        ...f444e44deff.......
        ...fffffeeef.........
        ..ffffffff...........
        ..fff..ff............
        `)
    anim.addAnimationFrame(img`
        .....fff.............
        ....fff2ff...........
        ..ffeeef2ff..........
        .ffeeeef2eff.........
        .feeeeffeeeef....fff.
        .fffffe22222f...fccf.
        .ffe222ffff2f..fccbf.
        ffffffffeeeff.feccbf.
        fefe441ff4eeffeecbf..
        ffee4d4bdddeffeeff...
        .ffeee4dddeedeef.....
        ..ff2222eeddeef......
        ...f444e44deff.......
        ...fffffeeef.........
        ..ffffffff...........
        ..fff..ff............
        `)
    anim.addAnimationFrame(img`
        .......ff............
        ....ffff2ff..........
        ..ffeeeef2ff.........
        .ffeeeeef22ff........
        .feeeeffeeeef........
        .fffffee2222ef.......
        fffe222ffffe2f.......
        ffffffffeeefff.......
        fefe44ebf44eef.......
        .fee4d4bfddef....fff.
        ..feee4dddeedffffcccf
        ...f2222eeddeeeeecccc
        ...f444e44ddedfffbbbf
        ...fffffeeeeff..fbbf.
        ..ffffffffff....fff..
        ..fff..ff............
        `)
    anim.addAnimationFrame(img`
        .......ff............
        ....ffff2ff..........
        ..ffeeeef2ff.........
        .ffeeeeef22ff........
        .feeeeffeeeef........
        .fffffee2222ef.......
        fffe222ffffe2f.......
        ffffffffeeefff.......
        fefe44ebf44eef.......
        .fee4d4bfddef........
        ..feee4dddeeef.......
        ...f2222eeddedf......
        ...f444e44ddeef......
        ...fffffeeeeebcf.....
        ..fffffffffffccf.....
        ..fff..ff....ff......
        .....................
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.SwingAxLeft, 100)
    anim.addAnimationFrame(img`
        .............fff.....
        ...........ff2fff....
        ..........ff2feeeff..
        .........ffe2feeeeff.
        .fff....feeeeffeeeef.
        .fccf...f22222efffff.
        .fbccf..f2ffff222eff.
        .fbccef.ffeeeffffffff
        ..fbceeffee4ff144efef
        ...ffeeffedddb4d4eeff
        .....feedeeddd4eeeff.
        ......feeddee2222ff..
        .......ffed44e444f...
        .........feeefffff...
        ...........ffffffff..
        ............ff..fff..
        `)
    anim.addAnimationFrame(img`
        .............fff.....
        ...........ff2fff....
        ..........ff2feeeff..
        .........ffe2feeeeff.
        .fff....feeeeffeeeef.
        .fccf...f22222efffff.
        .fbccf..f2ffff222eff.
        .fbccef.ffeeeffffffff
        ..fbceeffee4ff144efef
        ...ffeeffedddb4d4eeff
        .....feedeeddd4eeeff.
        ......feeddee2222ff..
        .......ffed44e444f...
        .........feeefffff...
        ...........ffffffff..
        ............ff..fff..
        `)
    anim.addAnimationFrame(img`
        ............ff.......
        ..........ff2ffff....
        .........ff2feeeeff..
        ........ff22feeeeeff.
        ........feeeeffeeeef.
        .......fe2222eefffff.
        .......f2effff222efff
        .......fffeeeffffffff
        .......fee44fbe44efef
        .fff....feddfb4d4eef.
        fcccffffdeeddd4eeef..
        cccceeeeeddee2222f...
        fbbbfffdedd44e444f...
        .fbbf..ffeeeefffff...
        ..fff....ffffffffff..
        ............ff..fff..
        `)
    anim.addAnimationFrame(img`
        ............ff.......
        ..........ff2ffff....
        .........ff2feeeeff..
        ........ff22feeeeeff.
        ........feeeeffeeeef.
        .......fe2222eefffff.
        .......f2effff222efff
        .......fffeeeffffffff
        .......fee44fbe44efef
        ........feddfb4d4eef.
        .......feeeddd4eeef..
        ......fdeddee2222f...
        ......feedd44e444f...
        .....fcbeeeeefffff...
        .....fccfffffffffff..
        ......ff....ff..fff..
        .....................
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.SwingAxDown, 100)
    anim.addAnimationFrame(img`
        ...........ff...........
        ..........fcbf..........
        ......fffffcbf..........
        .....f2222fcf...........
        ...ff222222ef...........
        ..fff222222eff..........
        ..feeeeeeeeeef..........
        ..fe2222222eeff.........
        .fffffeeeef4eff.........
        .ffefbf44fb44ff.........
        ..fe41fddf14fff.........
        ..fff4dddd44ff..........
        ...fe444444efe..........
        ..fef222222ef...........
        ..f4f445544ef...........
        ...fffffffff............
        .....fff.ff.............
        ........................
        ........................
        ........................
        `)
    anim.addAnimationFrame(img`
        ...........ff...........
        ..........fcbf..........
        .......ff.fcbf..........
        .....ff22ffcf...........
        ...fff2222fef...........
        ..fff222222eff..........
        ..fff222222eff..........
        ..feeeeeeeeeeff.........
        .ffe22222224eff.........
        .fffffeeeef44ff.........
        ..fefbf44fb44ff.........
        ..fe41fddf14ff..........
        ...fe4dddd4efe..........
        ..fef222222ef...........
        ..f4f445544ef...........
        ...fffffffff............
        .....fff.ff.............
        ........................
        ........................
        ........................
        ........................
        ........................
        ........................
        ........................
        `)
    anim.addAnimationFrame(img`
        .......ff...............
        .....ff22ff.............
        ...fff2222fff...........
        ..fff222222fff..........
        ..fff222222fff..........
        ..feeeeeeeeeeff.........
        .ffe22222222eff.........
        .fffffeeeefffff.........
        ..fefbf44fbfeff.........
        ..fe41fddf14ef..........
        ...fe4dddd4efe..........
        ..fef22222fcc...........
        ..f4f44554fb............
        ...ffffffffb............
        .....ff.ff..............
        ........................
        ........................
        ........................
        ........................
        ........................
        `)
    anim.addAnimationFrame(img`
        .......ff...............
        .....ff22ff.............
        ...fff2222fff...........
        ..fff222222fff..........
        ..fff222222fff..........
        ..feeeeeeeeeeff.........
        .ffe22222222eff.........
        .fffffeeeefffff.........
        ..fefbf44fbfeff.........
        ..fe41fddf14ef..........
        ...fe4dddd4efe..........
        ..fef22222f4f...........
        ..f4f44554f4f...........
        ...fffffddff............
        .....ffeeff.............
        ....ffeef...............
        ...fbbeef...............
        ...fbccf................
        ...fccf.................
        ....ff..................
        `)
    animation.attachAnimation(playerSprite, anim)
    anim = animation.createAnimation(ActionKind.SwingAxUp, 100)
    anim.addAnimationFrame(img`
        ...................ff...
        .........ffff.....fbcf..
        .......ffeeeeff..fbcccf.
        ......feeeffeeef..fecf..
        .....fffff22ffffffeef...
        .....ffe2e22e2effeef....
        .....fe2f2ff2f2efef.....
        .....fff22ee22ffff......
        ....ffef2feef2feff......
        ....feeffeeeefeeef......
        .....feeeeeeeeeef4......
        ......feeeeeeeef4f......
        .....f4ffffffff2f.......
        ......ff222222ff........
        .......f444444f.........
        ........ffffff..........
        ........ff..ff..........
        `)
    anim.addAnimationFrame(img`
        ...................ff...
        .........ffff.....fbcf..
        .......ffeeeeff..fbcccf.
        ......feeeffeeef..fecf..
        .....fffff22ffffffeef...
        .....ffe2e22e2effeef....
        .....fe2f2ff2f2efef.....
        .....fff22ee22ffff......
        ....ffef2feef2feff......
        ....feeffeeeefeeef......
        .....feeeeeeeeeef4......
        ......feeeeeeeef4f......
        .....f4ffffffff2f.......
        ......ff222222ff........
        .......f444444f.........
        ........ffffff..........
        ........ff..ff..........
        `)
    anim.addAnimationFrame(img`
        ........................
        ..........ffff..........
        ........ffeeeeff........
        .......feeeffeeef.......
        ......fffff22fffff......
        ......ffe2e22e2eff......
        ......fe2f2ff2f2ef......
        ......fff22ee22fff......
        .....ffef2feef2feff.....
        .....feeffeeeefeeef.....
        ......feeeeeeeeeef......
        .......feeeeeeeef.......
        ......e4ffffffff4e......
        ......4df222222fd4......
        ......44f444444f44......
        .........ffffff.........
        .........ff..ff.........
        `)
    anim.addAnimationFrame(img`
        ........................
        ..........ffff..........
        ........ffeeeeff........
        .......feeeffeeef.......
        ......fffff22fffff......
        ......ffe2e22e2eff......
        ......fe2f2ff2f2ef......
        ......fff22ee22fff......
        .....ffef2feef2feff.....
        ....ffeeffeeeefeeef.....
        ...feffeeeeeeeeeef......
        ..fcceffeeeeeeeef.......
        .fcccfe4ffffffff4.......
        .fbcf.fdf222222f........
        ..ff...ff444444f........
        .........ffffff.........
        .........ff..ff.........
        `)
    animation.attachAnimation(playerSprite, anim)
}
function plantFood () {
    if (supplyInventory.indexOf(activeSupply) >= 0) {
        if (activeSupply == "carrot") {
            plantCarrot()
        }
    }
}
controller.up.onEvent(ControllerButtonEvent.Released, function () {
    if (!(controller.B.isPressed())) {
        if (controller.left.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
        } else if (controller.down.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        } else if (controller.right.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
        }
    }
})
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile24`, function (sprite, location) {
    if (eventTimerNames.indexOf("start fire") < 0) {
        if (wood > 0) {
            if (game.ask("Light the fire?")) {
                tiles.setTileAt(location, assets.tile`myTile25`)
                fire = sprites.create(img`
                    . . . . . . . 5 . . 5 . . . . . 
                    . . . . . . 4 . . . . 4 . . . . 
                    . . . . . 4 4 4 . 5 4 4 . . . . 
                    . . . . 4 4 5 5 4 5 4 4 . . . . 
                    . . . . 4 5 5 4 4 5 5 4 . . . . 
                    . . . 4 4 5 4 4 5 5 5 4 4 . . . 
                    . . 4 4 5 5 4 . 5 4 4 5 4 . . . 
                    . . 4 5 5 4 4 5 5 4 4 5 4 . . . 
                    . . . 5 2 4 5 5 4 . 5 5 4 . . . 
                    . . . 4 2 2 4 4 . 4 4 5 4 . . . 
                    . . . 4 4 2 2 2 2 2 5 2 4 4 . . 
                    . . . . 4 4 4 4 4 4 2 2 4 . . . 
                    . . . . 4 4 4 4 4 4 . 4 . . . . 
                    . . . . . 4 4 . . 4 4 4 . . . . 
                    . . . . . . . . . . . . . . . . 
                    . . . . . . . . . . . . . . . . 
                    `, SpriteKind.Player)
                tiles.placeOnTile(fire, location)
                fire.startEffect(effects.fire)
            }
        } else {
            playerSprite.sayText("I need to gather some wood to start a fire", 2000, true)
        }
        setEventTimer("start fire", 20)
    }
})
function harvestCarrot () {
    if (playerSprite.tileKindAt(TileDirection.Center, assets.tile`myTile5`)) {
        supplyInvCount[supplyInventory.indexOf("carrot")] = supplyInvCount[supplyInventory.indexOf("carrot")] + 4
        tiles.setTileAt(playerSprite.tilemapLocation(), assets.tile`myTile`)
        locationTypes[modifiedLocations.indexOf(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)] = 1
        saveGame()
    }
}
function chopTrees () {
    if (playerFacing == "left") {
        if (playerSprite.tileKindAt(TileDirection.Left, assets.tile`myTile1`)) {
            chopTree(playerSprite.tilemapLocation().column - 1, playerSprite.tilemapLocation().row)
        }
    } else if (playerFacing == "right") {
        if (playerSprite.tileKindAt(TileDirection.Right, assets.tile`myTile1`)) {
            chopTree(playerSprite.tilemapLocation().column + 1, playerSprite.tilemapLocation().row)
        }
    } else if (playerFacing == "up") {
        if (playerSprite.tileKindAt(TileDirection.Top, assets.tile`myTile1`)) {
            chopTree(playerSprite.tilemapLocation().column, playerSprite.tilemapLocation().row - 1)
        }
    } else {
        if (playerSprite.tileKindAt(TileDirection.Bottom, assets.tile`myTile1`)) {
            chopTree(playerSprite.tilemapLocation().column, playerSprite.tilemapLocation().row + 1)
        }
    }
}
function plantCarrot () {
    if (supplyInvCount[supplyInventory.indexOf("carrot")] > 0) {
        tiles.setTileAt(playerSprite.tilemapLocation(), assets.tile`myTile4`)
        supplyInvCount[0] = supplyInvCount[0] - 1
        timedLocations.push(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)
        locationTimers.push(gameStepCount + 600)
        timedTypes.push(4)
        locationTypes.removeAt(modifiedLocations.indexOf(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row))
        modifiedLocations.removeAt(modifiedLocations.indexOf(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row))
        if (!(blockSettings.exists("hasPlanted"))) {
            blockSettings.writeString("hasPlanted", "true")
        }
        saveGame()
    }
}
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    if (controller.B.isPressed()) {
        if (toolInventory.length > 1) {
            menuSprites[toolInventory.indexOf(activeTool)].setImage(toolIcons[toolIndex.indexOf(activeTool)])
            activeTool = toolInventory[(toolInventory.indexOf(activeTool) + toolInventory.length - 1) % toolInventory.length]
            menuSprites[toolInventory.indexOf(activeTool)].setImage(activeToolIcons[toolIndex.indexOf(activeTool)])
        }
    } else if (controller.A.isPressed() && activeTool == "shovel") {
        if (supplyInventory.length > 1) {
            supplyMenuSprites[supplyInventory.indexOf(activeSupply)].setBorder(1, 1)
            activeSupply = supplyInventory[(supplyInventory.indexOf(activeSupply) + supplyInventory.length - 1) % supplyInventory.length]
            supplyMenuSprites[supplyInventory.indexOf(activeSupply)].setBorder(1, 5)
        }
    } else {
        animation.setAction(playerSprite, ActionKind.WalkLeft)
        playerFacing = "left"
    }
})
function saveGame () {
    blockSettings.writeNumber("gameStepCount", gameStepCount)
    blockSettings.writeNumberArray("timedLocations", timedLocations)
    blockSettings.writeNumberArray("locationTimers", locationTimers)
    blockSettings.writeNumberArray("timedTypes", timedTypes)
    blockSettings.writeNumberArray("modifiedLocations", modifiedLocations)
    blockSettings.writeNumberArray("locationTypes", locationTypes)
    saveInventory()
}
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    if (controller.B.isPressed()) {
        if (toolInventory.length > 1) {
            menuSprites[toolInventory.indexOf(activeTool)].setImage(toolIcons[toolIndex.indexOf(activeTool)])
            activeTool = toolInventory[(toolInventory.indexOf(activeTool) + 1) % toolInventory.length]
            menuSprites[toolInventory.indexOf(activeTool)].setImage(activeToolIcons[toolIndex.indexOf(activeTool)])
        }
    } else if (controller.A.isPressed() && activeTool == "shovel") {
        if (supplyInventory.length > 1) {
            supplyMenuSprites[supplyInventory.indexOf(activeSupply)].setBorder(1, 1)
            activeSupply = supplyInventory[(supplyInventory.indexOf(activeSupply) + supplyInventory.length + 1) % supplyInventory.length]
            supplyMenuSprites[supplyInventory.indexOf(activeSupply)].setBorder(1, 5)
        }
    } else {
        animation.setAction(playerSprite, ActionKind.WalkRight)
        playerFacing = "right"
    }
})
function usePick () {
    if (tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile22`) || tiles.tileAtLocationEquals(playerSprite.tilemapLocation(), assets.tile`myTile27`)) {
        modifiedLocations.push(playerSprite.tilemapLocation().column * 100 + playerSprite.tilemapLocation().row)
        locationTypes.push(tileIndex.indexOf(sprites.castle.tilePath5))
        tiles.setTileAt(playerSprite.tilemapLocation(), sprites.castle.tilePath5)
        if (supplyInventory.indexOf("stone") < 0) {
            supplyInventory.push("stone")
            supplyInvCount.push(2)
            game.splash("You've collected some stone")
        } else {
            supplyInvCount[supplyInventory.indexOf("stone")] = supplyInvCount[supplyInventory.indexOf("stone")] + 2
        }
        saveGame()
    }
}
controller.B.onEvent(ControllerButtonEvent.Pressed, function () {
    controller.moveSprite(playerSprite, 0, 0)
    showToolMenu()
})
function savePlayerInfo () {
    blockSettings.writeNumber("health", info.life())
    blockSettings.writeNumber("score", info.score())
    blockSettings.writeNumber("playerX", playerSprite.x)
    blockSettings.writeNumber("playerY", playerSprite.y)
    blockSettings.writeNumber("gameStepCount", gameStepCount)
    blockSettings.writeString("activeTool", activeTool)
}
function getPxDistTo (sprite1: Sprite, sprite2: Sprite) {
    return Math.sqrt((sprite1.x - sprite2.x) * (sprite1.x - sprite2.x) + (sprite1.y - sprite2.y) * (sprite1.y - sprite2.y))
}
function setEventTimer (name: string, gameSteps: number) {
    if (eventTimerNames.indexOf(name) >= 0) {
        eventTimers[eventTimerNames.indexOf(name)] = gameStepCount + gameSteps
    } else {
        eventTimerNames.push(name)
        eventTimers.push(gameStepCount + gameSteps)
    }
}
function hasTimerEnded (name: string) {
    return eventTimerNames.indexOf(name) < 0
}
scene.onOverlapTile(SpriteKind.Player, assets.tile`myTile`, function (sprite, location) {
    if (activeTool == "shovel") {
        if (hasTimerEnded("food prompt")) {
            if (!(blockSettings.exists("hasPlanted"))) {
                tiles.placeOnTile(helperSprite, location)
                helperSprite.sayText("Hold A to open planting menu", 2000, false)
            } else if (!(blockSettings.exists("hasBoughtFood"))) {
                playerSprite.sayText("I could by more to plant in town", 2000, true)
            }
            setEventTimer("food prompt", 50)
        }
    }
})
function chopTree (col: number, row: number) {
    tiles.setTileAt(tiles.getTileLocation(col, row), assets.tile`myTile2`)
    tiles.setWallAt(tiles.getTileLocation(col, row), false)
    timedLocations.push(col * 100 + row)
    locationTimers.push(gameStepCount + 6000)
    timedTypes.push(2)
    wood += 5
    saveGame()
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    if (controller.A.isPressed() && activeTool == "shovel") {
    	
    } else if (!(controller.B.isPressed())) {
        if (!(controller.left.isPressed() || controller.right.isPressed())) {
            animation.setAction(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        }
    } else {
    	
    }
})
function saveInventory () {
    blockSettings.writeNumber("wood", wood)
    blockSettings.writeNumber("cashMoney", cashMoney)
    blockSettings.writeNumberArray("foodInventory", supplyInvCount)
    savePlayerInfo()
}
controller.down.onEvent(ControllerButtonEvent.Released, function () {
    if (!(controller.B.isPressed())) {
        if (controller.up.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        } else if (controller.left.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
        } else if (controller.right.isPressed()) {
            animation.setAction(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
        }
    }
})
function hideToolMenu () {
    let selectedTool = ""
    for (let index = 0; index <= menuSprites.length - 1; index++) {
        sprites.destroy(menuSprites[index])
    }
    for (let index = 0; index <= textSprites.length - 1; index++) {
        sprites.destroy(textSprites[index])
    }
    toolSprite.setImage(toolIcons[toolIndex.indexOf(selectedTool)])
    toolSprite.setPosition(scene.cameraProperty(CameraProperty.X), scene.cameraProperty(CameraProperty.Bottom) - 8)
    sprites.destroy(infoBgSprite)
}
let anim: animation.Animation = null
let infoBgSprite: Sprite = null
let textSprites: TextSprite[] = []
let menuSprite: Sprite = null
let menuSprites: Sprite[] = []
let eventTimerNames: string[] = []
let eventTimers: number[] = []
let activeToolIcons: Image[] = []
let toolIndex: string[] = []
let toolIcons: Image[] = []
let wood = 0
let row = 0
let col = 0
let timedTypes: number[] = []
let toolInventory: string[] = []
let snake: Sprite = null
let maxEnemies = 0
let enemyList: Sprite[] = []
let cashMoney = 0
let answer = 0
let shopIsOpen = false
let tileIndex: Image[] = []
let locationTypes: number[] = []
let modifiedLocations: number[] = []
let timedLocations: number[] = []
let locationTimers: number[] = []
let gameStepCount = 0
let activeSupply = ""
let supplyIndex: string[] = []
let supplyIcons: Image[] = []
let supplyInvCount: number[] = []
let textSprite: TextSprite = null
let supplyInventory: string[] = []
let prevX = 0
let supplyMenuSprites: TextSprite[] = []
let activeTool = ""
let yesnoAnswer = false
let toolSprite: Sprite = null
let playerFacing = ""
let playerSprite: Sprite = null
let fire: Sprite = null
let blacksmith: Sprite = null
let helperSprite: Sprite = null
let farmer: Sprite = null
tiles.setCurrentTilemap(tilemap`level2`)
let home = sprites.create(assets.image`myImage`, SpriteKind.structure)
tiles.placeOnTile(home, tiles.getTileLocation(21, 83))
farmer = sprites.create(img`
    . . . . . . f f f f . . . . . . 
    . . . . f f f 8 8 f f f . . . . 
    . . . f f 8 8 8 8 8 8 f f . . . 
    . . f f 8 e e e e e e 8 f f . . 
    . . f e e 8 8 8 8 8 8 e e f . . 
    . . f e 8 f f f f f f 8 e f . . 
    . . f f f f e e e e f f f f . . 
    . f f e f 7 f 4 4 f 7 f e f f . 
    . f e e 4 1 f d d f 1 4 e e f . 
    . . f e e d d d d d d e e f . . 
    . . . f e e 4 4 4 4 e e f . . . 
    . . 8 4 f 8 8 8 8 8 8 f 4 8 . . 
    . . 4 d f 8 8 8 8 8 8 f d 4 . . 
    . . 4 4 f b b 5 5 b b f 4 4 . . 
    . . . . . 8 8 8 8 8 8 . . . . . 
    . . . . . 8 8 . . 8 8 . . . . . 
    `, SpriteKind.npc)
tiles.placeOnTile(farmer, tiles.getTileLocation(20, 22))
farmer.setFlag(SpriteFlag.GhostThroughWalls, true)
helperSprite = sprites.create(img`
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    `, SpriteKind.npc)
blacksmith = sprites.create(img`
    . . . . . . f f f f . . . . . . 
    . . . . f f f 8 8 f f f . . . . 
    . . . f f 8 8 8 8 8 8 f f . . . 
    . . f f 8 e e e e e e 8 f f . . 
    . . f e e 8 8 8 8 8 8 e e f . . 
    . . f e 8 f f f f f f 8 e f . . 
    . . f f f f e e e e f f f f . . 
    . f f e f 7 f 4 4 f 7 f e f f . 
    . f e e 4 1 f d d f 1 4 e e f . 
    . . f e e d d d d d d e e f . . 
    . . . f e e 4 4 4 4 e e f . . . 
    . . 8 4 f 8 8 8 8 8 8 f 4 8 . . 
    . . 4 d f 8 8 8 8 8 8 f d 4 . . 
    . . 4 4 f b b 5 5 b b f 4 4 . . 
    . . . . . 8 8 8 8 8 8 . . . . . 
    . . . . . 8 8 . . 8 8 . . . . . 
    `, SpriteKind.npc)
tiles.placeOnTile(blacksmith, tiles.getTileLocation(17, 26))
blacksmith.setFlag(SpriteFlag.GhostThroughWalls, true)
fire = sprites.create(img`
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    . . . . . . . . . . . . . . . . 
    `, SpriteKind.Player)
playerSprite = sprites.create(img`
    . . . . . . f f f f . . . . . . 
    . . . . f f f 2 2 f f f . . . . 
    . . . f f f 2 2 2 2 f f f . . . 
    . . f f f e e e e e e f f f . . 
    . . f f e 2 2 2 2 2 2 e e f . . 
    . . f e 2 f f f f f f 2 e f . . 
    . . f f f f e e e e f f f f . . 
    . f f e f b f 4 4 f b f e f f . 
    . f e e 4 1 f d d f 1 4 e e f . 
    . . f e e d d d d d d e e f . . 
    . . . f e e 4 4 4 4 e e f . . . 
    . . e 4 f 2 2 2 2 2 2 f 4 e . . 
    . . 4 d f 2 2 2 2 2 2 f d 4 . . 
    . . 4 4 f 4 4 5 5 4 4 f 4 4 . . 
    . . . . . f f f f f f . . . . . 
    . . . . . f f . . f f . . . . . 
    `, SpriteKind.Player)
playerFacing = "down"
tiles.placeOnTile(playerSprite, tiles.getTileLocation(26, 85))
controller.moveSprite(playerSprite, 50, 50)
scene.cameraFollowSprite(playerSprite)
setupCharacterAnim()
toolSprite = sprites.create(assets.image`hand icon inactive`, SpriteKind.Menu)
toolSprite.setFlag(SpriteFlag.GhostThroughWalls, true)
initGameData()
if (blockSettings.exists("gameStepCount")) {
    yesnoAnswer = false
    while (yesnoAnswer == false) {
        yesnoAnswer = game.ask("Load previous save?")
        if (yesnoAnswer == true) {
            loadSave()
        } else {
            yesnoAnswer = game.ask("Start a new game", "and erase save?")
            if (yesnoAnswer == true) {
                blockSettings.clear()
            }
        }
    }
} else {
	
}
game.onUpdateInterval(100, function () {
    gameStepCount += 1
    playBeginning()
    for (let index = 0; index <= locationTimers.length - 1; index++) {
        if (gameStepCount >= locationTimers[index]) {
            if (timedTypes[index] == 4) {
                tiles.setTileAt(tiles.getTileLocation(Math.idiv(timedLocations[index], 100), timedLocations[index] % 100), assets.tile`myTile5`)
                modifiedLocations.push(timedLocations[index])
                locationTypes.push(5)
                locationTimers.removeAt(index)
                timedTypes.removeAt(index)
                timedLocations.removeAt(index)
                index += -1
                saveGame()
            } else if (timedTypes[index] == 2) {
                tiles.setTileAt(tiles.getTileLocation(Math.idiv(timedLocations[index], 100), timedLocations[index] % 100), assets.tile`myTile1`)
                locationTimers.removeAt(index)
                timedTypes.removeAt(index)
                timedLocations.removeAt(index)
                index += -1
                saveGame()
            }
        }
    }
    for (let index = 0; index <= eventTimers.length - 1; index++) {
        if (gameStepCount >= eventTimers[index]) {
            eventTimerNames.removeAt(index)
            eventTimers.removeAt(index)
        }
    }
})
game.onUpdate(function () {
    if (playerSprite.vx == 0 && (playerSprite.vy == 0 && !(controller.A.isPressed()))) {
        animation.stopAnimation(animation.AnimationTypes.All, playerSprite)
    }
    if (!(controller.B.isPressed())) {
        toolSprite.setPosition(scene.cameraProperty(CameraProperty.X), scene.cameraProperty(CameraProperty.Bottom) - 8)
    }
    for (let index = 0; index <= enemyList.length - 1; index++) {
        if (getPxDistTo(playerSprite, enemyList[index]) > 180) {
            sprites.destroy(enemyList.removeAt(index))
            index += -1
            playerSprite.sayText("I think I got away", 1000, false)
        }
    }
})
