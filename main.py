class ActionKind(Enum):
    Walking = 0
    Idle = 1
    Jumping = 2
    WalkRight = 3
    WalkDown = 4
    WalkLeft = 5
    WalkUp = 6
    SwingAxRight = 7
    SwingAxLeft = 8
    SwingAxDown = 9
    SwingAxUp = 10
@namespace
class SpriteKind:
    Menu = SpriteKind.create()
    npc = SpriteKind.create()
    coin = SpriteKind.create()
    structure = SpriteKind.create()
def useShovel():
    prepareGround()

def on_on_overlap(sprite, otherSprite):
    global activeTool
    if controller.A.is_pressed():
        sprites.destroy(otherSprite, effects.disintegrate, 500)
        activeTool = "ax"
        info.change_score_by(10)
        savePlayerInfo()
    else:
        scene.camera_shake(4, 500)
        otherSprite.x += 32
        otherSprite.y += 32
        info.change_life_by(-1)
        savePlayerInfo()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

def showSupplyMenu():
    global supplyMenuSprites, textSprite
    controller.move_sprite(playerSprite, 0, 0)
    supplyMenuSprites = []
    index = 0
    while index <= len(supplyInventory) - 1:
        textSprite = textsprite.create("" + str(supplyInvCount[index]), 1, 15)
        textSprite.set_icon(supplyIcons[supplyIndex.index(supplyInventory[index])])
        if supplyInventory[index] == activeSupply:
            textSprite.set_border(1, 5)
        else:
            textSprite.set_border(1, 1)
        textSprite.set_position(scene.camera_property(CameraProperty.X) + index * 16,
            scene.camera_property(CameraProperty.BOTTOM) - 24)
        supplyMenuSprites.append(textSprite)
        index += 1
def playBeginning():
    if gameStepCount == 20:
        playerSprite.say_text("I can't believe the deal I got on this land", 5000, True)
    elif gameStepCount == 110:
        playerSprite.say_text("I should plant the last of my food.", 5000, True)
    elif gameStepCount == 160:
        playerSprite.say_text("I can sell what I grow in town", 5000, True)
    else:
        pass
def isInFarm():
    return playerSprite.tilemap_location().column < 39 and playerSprite.tilemap_location().column > 12 and (playerSprite.tilemap_location().row < 93 and playerSprite.tilemap_location().row > 73)

def on_overlap_tile(sprite2, location):
    tiles.place_on_tile(helperSprite, location)
    helperSprite.say_text("" + str(Math.idiv(locationTimers[timedLocations.index(location.column * 100 + location.row)] - gameStepCount,
            10)) + "s",
        1000,
        False)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile4
    """),
    on_overlap_tile)

def on_up_pressed():
    global playerFacing
    if controller.A.is_pressed() and activeTool == "shovel":
        pass
    elif not (controller.B.is_pressed()):
        if not (controller.left.is_pressed() or controller.right.is_pressed()):
            animation.set_action(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
    else:
        pass
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def prepareGround():
    if playerSprite.tilemap_location().column < 39 and playerSprite.tilemap_location().column > 12:
        if tiles.tile_at_location_equals(playerSprite.tilemap_location(), sprites.castle.tile_grass1) or (tiles.tile_at_location_equals(playerSprite.tilemap_location(), sprites.castle.tile_grass3) or tiles.tile_at_location_equals(playerSprite.tilemap_location(), sprites.castle.tile_path5)):
            modifiedLocations.append(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row)
            locationTypes.append(tileIndex.index(assets.tile("""
                myTile
            """)))
            tiles.set_tile_at(playerSprite.tilemap_location(),
                assets.tile("""
                    myTile
                """))
            saveGame()
        elif tiles.tile_at_location_equals(playerSprite.tilemap_location(),
            assets.tile("""
                myTile20
            """)) or tiles.tile_at_location_equals(playerSprite.tilemap_location(),
            assets.tile("""
                myTile2
            """)):
            modifiedLocations.append(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row)
            locationTypes.append(tileIndex.index(sprites.castle.tile_grass1))
            tiles.set_tile_at(playerSprite.tilemap_location(), sprites.castle.tile_grass1)
        elif tiles.tile_at_location_equals(playerSprite.tilemap_location(),
            assets.tile("""
                myTile21
            """)):
            modifiedLocations.append(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row)
            locationTypes.append(tileIndex.index(sprites.castle.tile_path5))
            tiles.set_tile_at(playerSprite.tilemap_location(), sprites.castle.tile_path5)
        else:
            pass

def on_a_pressed():
    if False:
        pass
    elif activeTool == "ax":
        if playerFacing == "right":
            animation.set_action(playerSprite, ActionKind.SwingAxRight)
        elif playerFacing == "left":
            animation.set_action(playerSprite, ActionKind.SwingAxLeft)
        elif playerFacing == "down":
            animation.set_action(playerSprite, ActionKind.SwingAxDown)
        else:
            animation.set_action(playerSprite, ActionKind.SwingAxUp)
        chopTrees()
    elif isInFarm():
        if activeTool == "shovel":
            if playerSprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
                myTile
            """)):
                showSupplyMenu()
        elif activeTool == "hammer":
            build()
    else:
        pass
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_left_released():
    global playerFacing
    if not (controller.B.is_pressed()):
        if controller.up.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        elif controller.down.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        elif controller.right.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
controller.left.on_event(ControllerButtonEvent.RELEASED, on_left_released)

def on_b_released():
    controller.move_sprite(playerSprite, 50, 50)
    hideToolMenu()
    savePlayerInfo()
controller.B.on_event(ControllerButtonEvent.RELEASED, on_b_released)

def on_a_released():
    hideSupplyMenu()
    if playerSprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
        myTile5
    """)):
        harvestCarrot()
    elif activeTool == "shovel" and isInFarm():
        if playerSprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
            myTile
        """)):
            plantFood()
        else:
            useShovel()
controller.A.on_event(ControllerButtonEvent.RELEASED, on_a_released)

def hideSupplyMenu():
    global supplyMenuSprites
    controller.move_sprite(playerSprite, 50, 50)
    for value in supplyMenuSprites:
        sprites.destroy(value)
    supplyMenuSprites = []

def on_overlap_tile2(sprite3, location2):
    global shopIsOpen, answer, cashMoney
    if not (shopIsOpen):
        farmer.say_text("Carrots for sale (A)", 100, False)
        if controller.A.is_pressed():
            shopIsOpen = True
            tiles.place_on_tile(playerSprite,
                tiles.get_tile_location(location2.column, location2.row + 2))
            answer = game.ask_for_number("How many would you like to buy? ($3 each)")
            if answer > 0:
                if 3 * answer <= cashMoney:
                    cashMoney = cashMoney - 3 * answer
                    supplyInvCount[0] = supplyInvCount[0] + answer
                    if not (blockSettings.exists("hasBoughtFood")):
                        blockSettings.write_string("hasBoughtFood", "true")
                    saveInventory()
                    farmer.say_text("Thank you, Have a nice day!", 2000, False)
                else:
                    farmer.say_text("You don't have enough money", 2000, False)
            else:
                farmer.say_text("Have a nice day!", 2000, False)
            shopIsOpen = False
    else:
        tiles.place_on_tile(playerSprite,
            tiles.get_tile_location(location2.column, location2.row + 2))
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile11
    """),
    on_overlap_tile2)

def build():
    if tiles.tile_at_location_equals(playerSprite.tilemap_location(),
        assets.tile("""
            myTile
        """)):
        tiles.set_tile_at(playerSprite.tilemap_location(),
            assets.tile("""
                myTile3
            """))
        tiles.set_wall_at(playerSprite.tilemap_location(), True)
        modifiedLocations.append(col2 * 100 + row2)
        locationTypes.append(3)
        saveGame()

def on_right_released():
    global playerFacing
    if not (controller.B.is_pressed()):
        if controller.up.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        elif controller.down.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        elif controller.left.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
controller.right.on_event(ControllerButtonEvent.RELEASED, on_right_released)

def on_overlap_tile3(sprite4, location3):
    global snake
    if hasTimerEnded("bushTriggerDelay"):
        if Math.percent_chance(25) and len(enemyList) < maxEnemies:
            snake = sprites.create(img("""
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
                """),
                SpriteKind.enemy)
            snake.set_position(playerSprite.x + 24, playerSprite.y + 24)
            animation.run_image_animation(snake,
                [img("""
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
                    """),
                    img("""
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
                    """)],
                200,
                True)
            animation.run_movement_animation(snake,
                animation.animation_presets(animation.shake),
                200,
                False)
            snake.follow(playerSprite, 10)
            enemyList.append(snake)
            if not (blockSettings.exists("snake warning")):
                blockSettings.write_string("snake warning", "true")
                playerSprite.say_text("A snake ... run!!", 2000, False)
            elif False:
                pass
            elif toolInventory.index("ax") >= 0 and blockSettings.exists("kill snake ax"):
                playerSprite.say_text("I could kill it with my ax", 2000, False)
                blockSettings.write_number("kill snake ax", 1)
            else:
                pass
        elif isInFarm() and not (blockSettings.exists("snake grass shovel tip")):
            blockSettings.write_string("snake grass shovel tip", "true")
            playerSprite.say_text("I should dig up that snake den", 2000, False)
        elif not (isInFarm()) and not (blockSettings.exists("avoid snake grass tip")):
            blockSettings.write_string("avoid snake grass tip", "true")
            playerSprite.say_text("I should watch out for snake dens", 2000, False)
        else:
            pass
    setEventTimer("bushTriggerDelay", 20)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile21
    """),
    on_overlap_tile3)

def on_overlap_tile4(sprite5, location4):
    global shopIsOpen, answer, cashMoney
    if not (shopIsOpen):
        farmer.say_text("Want to sell some food? (A)", 100, False)
        if controller.A.is_pressed():
            shopIsOpen = True
            tiles.place_on_tile(playerSprite,
                tiles.get_tile_location(location4.column, location4.row + 2))
            answer = game.ask_for_number("How many would you like to sell? ($2 each)")
            if answer > 0:
                if answer <= supplyInvCount[0]:
                    cashMoney = cashMoney + answer * 2
                    supplyInvCount[0] = supplyInvCount[0] - answer
                    saveInventory()
                    farmer.say_text("Thank you, Have a nice day!", 2000, False)
                else:
                    farmer.say_text("You don't have enough inventory", 2000, False)
            else:
                farmer.say_text("Have a nice day!", 2000, False)
            shopIsOpen = False
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile12
    """),
    on_overlap_tile4)

def loadSave():
    global timedLocations, timedTypes, locationTimers, col2, row2, modifiedLocations, locationTypes, gameStepCount, wood, supplyInvCount, cashMoney, activeTool
    if blockSettings.exists("timedLocations"):
        timedLocations = blockSettings.read_number_array("timedLocations")
        timedTypes = blockSettings.read_number_array("timedTypes")
        locationTimers = blockSettings.read_number_array("locationTimers")
        index2 = 0
        while index2 <= len(timedLocations):
            col2 = Math.idiv(timedLocations[index2], 100)
            row2 = timedLocations[index2] % 100
            if timedTypes[index2] == 2:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    assets.tile("""
                        myTile2
                    """))
                tiles.set_wall_at(tiles.get_tile_location(col2, row2), False)
            elif timedTypes[index2] == 4:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    assets.tile("""
                        myTile4
                    """))
            index2 += 1
    if blockSettings.exists("modifiedLocations"):
        modifiedLocations = blockSettings.read_number_array("modifiedLocations")
        locationTypes = blockSettings.read_number_array("locationTypes")
        index3 = 0
        while index3 <= len(modifiedLocations):
            col2 = Math.idiv(modifiedLocations[index3], 100)
            row2 = modifiedLocations[index3] % 100
            if locationTypes[index3] == 1:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    assets.tile("""
                        myTile
                    """))
            elif locationTypes[index3] == 3:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    assets.tile("""
                        myTile3
                    """))
                tiles.set_wall_at(tiles.get_tile_location(col2, row2), True)
            elif locationTypes[index3] == 5:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    assets.tile("""
                        myTile5
                    """))
            elif locationTypes[index3] == 0:
                tiles.set_tile_at(tiles.get_tile_location(col2, row2),
                    sprites.castle.tile_grass1)
            else:
                pass
            index3 += 1
    if blockSettings.exists("gameStepCount"):
        gameStepCount = blockSettings.read_number("gameStepCount")
    if blockSettings.exists("wood"):
        wood = blockSettings.read_number("wood")
    if blockSettings.exists("foodInventory"):
        supplyInvCount = blockSettings.read_number_array("foodInventory")
    if blockSettings.exists("playerX"):
        playerSprite.x = blockSettings.read_number("playerX")
        playerSprite.y = blockSettings.read_number("playerY")
    if blockSettings.exists("cashMoney"):
        cashMoney = blockSettings.read_number("cashMoney")
    if blockSettings.exists("score"):
        info.set_score(blockSettings.read_number("score"))
    if blockSettings.exists("activeTool"):
        activeTool = blockSettings.read_string("activeTool")
        toolSprite.set_image(toolIcons[toolIndex.index(activeTool)])

def on_overlap_tile5(sprite6, location5):
    global shopIsOpen, yesnoAnswer, cashMoney
    if not (shopIsOpen):
        blacksmith.say_text("Need a pick? (A)", 100, False)
        if controller.A.is_pressed():
            shopIsOpen = True
            tiles.place_on_tile(playerSprite,
                tiles.get_tile_location(location5.column + 2, location5.row))
            yesnoAnswer = game.ask("That will be $250")
            if yesnoAnswer:
                if 250 <= cashMoney:
                    cashMoney = cashMoney - 250
                    toolInventory.append("pick")
                    saveInventory()
                    farmer.say_text("Thank you, Have a nice day!", 2000, False)
                else:
                    farmer.say_text("You don't have enough money", 2000, False)
            else:
                farmer.say_text("Have a nice day!", 2000, False)
            shopIsOpen = False
    else:
        tiles.place_on_tile(playerSprite,
            tiles.get_tile_location(location5.column + 2, location5.row))
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile18
    """),
    on_overlap_tile5)

def on_overlap_tile6(sprite7, location6):
    tiles.place_on_tile(helperSprite, location6)
    helperSprite.say_text("Harvest (A)", 100, False)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile5
    """),
    on_overlap_tile6)

def initGameData():
    global activeTool, toolInventory, toolIndex, toolIcons, activeToolIcons, wood, supplyInvCount, supplyInventory, supplyIndex, supplyIcons, activeSupply, gameStepCount, timedLocations, locationTimers, timedTypes, modifiedLocations, locationTypes, shopIsOpen, cashMoney, maxEnemies, enemyList, eventTimers, eventTimerNames, tileIndex
    info.set_life(2)
    activeTool = "hand"
    toolInventory = ["hand", "shovel"]
    toolIndex = ["ax", "hammer", "shovel", "pick", "hand"]
    toolIcons = [assets.image("""
            ax icon inactive
        """),
        assets.image("""
            hammer icon inactive
        """),
        assets.image("""
            shovel icon inactive
        """),
        assets.image("""
            pick icon inactive
        """),
        assets.image("""
            hand icon inactive
        """)]
    activeToolIcons = [assets.image("""
            ax icon active
        """),
        assets.image("""
            hammer icon active
        """),
        assets.image("""
            shovel icon active
        """),
        assets.image("""
            pick icon active
        """),
        assets.image("""
            hand icon active
        """)]
    wood = 0
    supplyInvCount = [1, 0]
    supplyInventory = ["carrot", "wood"]
    supplyIndex = ["carrot", "wood"]
    supplyIcons = [assets.image("""
            carrot icon
        """),
        assets.image("""
            wood icon
        """)]
    activeSupply = "carrot"
    gameStepCount = 0
    timedLocations = []
    locationTimers = []
    timedTypes = []
    modifiedLocations = []
    locationTypes = []
    shopIsOpen = False
    cashMoney = 5
    info.set_score(0)
    maxEnemies = 1
    enemyList = []
    eventTimers = []
    eventTimerNames = []
    tileIndex = [assets.tile("""
            myTile5
        """),
        assets.tile("""
            myTile4
        """),
        assets.tile("""
            myTile
        """),
        assets.tile("""
            myTile21
        """),
        sprites.castle.tile_grass1,
        sprites.castle.tile_grass3,
        sprites.castle.tile_path5,
        assets.tile("""
            myTile27
        """),
        assets.tile("""
            myTile22
        """)]
def showToolMenu():
    global menuSprites, selectedTool, menuSprite, textSprites, infoBgSprite, textSprite
    menuSprites = []
    selectedTool = activeTool
    index4 = 0
    while index4 <= len(toolInventory) - 1:
        if toolInventory[index4] == selectedTool:
            menuSprite = sprites.create(activeToolIcons[toolIndex.index(toolInventory[index4])],
                SpriteKind.Menu)
            menuSprite.set_position(scene.camera_property(CameraProperty.X) + index4 * 16,
                scene.camera_property(CameraProperty.BOTTOM) - 24)
            menuSprites.append(menuSprite)
        else:
            menuSprite = sprites.create(toolIcons[toolIndex.index(toolInventory[index4])],
                SpriteKind.Menu)
            menuSprite.set_position(scene.camera_property(CameraProperty.X) + index4 * 16,
                scene.camera_property(CameraProperty.BOTTOM) - 24)
            menuSprites.append(menuSprite)
        index4 += 1
    textSprites = []
    infoBgSprite = sprites.create(img("""
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
        """),
        SpriteKind.text)
    infoBgSprite.set_position(scene.camera_property(CameraProperty.RIGHT) - infoBgSprite.width / 2,
        scene.camera_property(CameraProperty.TOP) + infoBgSprite.height)
    textSprite = textsprite.create("x" + str(cashMoney), 1, 15)
    textSprite.set_icon(img("""
        . . . b b . . . 
                . . b 5 5 b . . 
                . b 5 d 1 5 b . 
                . b 5 3 1 5 b . 
                . c 5 3 1 d c . 
                . c 5 1 d d c . 
                . . f d d f . . 
                . . . f f . . .
    """))
    textSprite.set_position(scene.camera_property(CameraProperty.RIGHT) - (textSprite.width / 2 + 4),
        scene.camera_property(CameraProperty.TOP) + 32)
    textSprites.append(textSprite)
    textSprite = textsprite.create("x" + str(supplyInvCount[0]), 1, 15)
    textSprite.set_icon(assets.image("""
        carrot icon
    """))
    textSprite.set_position(scene.camera_property(CameraProperty.RIGHT) - (textSprite.width / 2 + 4),
        scene.camera_property(CameraProperty.TOP) + 42)
    textSprites.append(textSprite)
def setupCharacterAnim():
    global anim
    anim = animation.create_animation(ActionKind.WalkDown, 200)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.WalkRight, 200)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.WalkLeft, 200)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.WalkUp, 200)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.SwingAxRight, 100)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.SwingAxLeft, 100)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.SwingAxDown, 100)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
    anim = animation.create_animation(ActionKind.SwingAxUp, 100)
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    anim.add_animation_frame(img("""
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
    """))
    animation.attach_animation(playerSprite, anim)
def plantFood():
    if supplyInventory.index(activeSupply) >= 0:
        if activeSupply == "carrot":
            plantCarrot()

def on_up_released():
    global playerFacing
    if not (controller.B.is_pressed()):
        if controller.left.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
        elif controller.down.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
        elif controller.right.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
controller.up.on_event(ControllerButtonEvent.RELEASED, on_up_released)

def on_overlap_tile7(sprite8, location7):
    global fire
    if eventTimerNames.index("start fire") < 0:
        if wood > 0:
            if game.ask("Light the fire?"):
                tiles.set_tile_at(location7, assets.tile("""
                    myTile25
                """))
                fire = sprites.create(img("""
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
                    """),
                    SpriteKind.player)
                tiles.place_on_tile(fire, location7)
                fire.start_effect(effects.fire)
        else:
            playerSprite.say_text("I need to gather some wood to start a fire", 2000, True)
        setEventTimer("start fire", 20)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile24
    """),
    on_overlap_tile7)

def harvestCarrot():
    if playerSprite.tile_kind_at(TileDirection.CENTER, assets.tile("""
        myTile5
    """)):
        supplyInvCount[supplyInventory.index("carrot")] = supplyInvCount[supplyInventory.index("carrot")] + 4
        tiles.set_tile_at(playerSprite.tilemap_location(),
            assets.tile("""
                myTile
            """))
        locationTypes[modifiedLocations.index(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row)] = 1
        saveGame()
def chopTrees():
    if playerFacing == "left":
        if playerSprite.tile_kind_at(TileDirection.LEFT, assets.tile("""
            myTile1
        """)):
            chopTree(playerSprite.tilemap_location().column - 1,
                playerSprite.tilemap_location().row)
    elif playerFacing == "right":
        if playerSprite.tile_kind_at(TileDirection.RIGHT, assets.tile("""
            myTile1
        """)):
            chopTree(playerSprite.tilemap_location().column + 1,
                playerSprite.tilemap_location().row)
    elif playerFacing == "up":
        if playerSprite.tile_kind_at(TileDirection.TOP, assets.tile("""
            myTile1
        """)):
            chopTree(playerSprite.tilemap_location().column,
                playerSprite.tilemap_location().row - 1)
    else:
        if playerSprite.tile_kind_at(TileDirection.BOTTOM, assets.tile("""
            myTile1
        """)):
            chopTree(playerSprite.tilemap_location().column,
                playerSprite.tilemap_location().row + 1)
def plantCarrot():
    if supplyInvCount[supplyInventory.index("carrot")] > 0:
        tiles.set_tile_at(playerSprite.tilemap_location(),
            assets.tile("""
                myTile4
            """))
        supplyInvCount[0] = supplyInvCount[0] - 1
        timedLocations.append(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row)
        locationTimers.append(gameStepCount + 600)
        timedTypes.append(4)
        locationTypes.remove_at(modifiedLocations.index(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row))
        modifiedLocations.remove_at(modifiedLocations.index(playerSprite.tilemap_location().column * 100 + playerSprite.tilemap_location().row))
        if not (blockSettings.exists("hasPlanted")):
            blockSettings.write_string("hasPlanted", "true")
        saveGame()

def on_left_pressed():
    global selectedTool, activeSupply, playerFacing
    if controller.B.is_pressed():
        if len(toolInventory) > 1:
            menuSprites[toolInventory.index(selectedTool)].set_image(toolIcons[toolIndex.index(selectedTool)])
            selectedTool = toolInventory[(toolInventory.index(selectedTool) + len(toolInventory) - 1) % len(toolInventory)]
            menuSprites[toolInventory.index(selectedTool)].set_image(activeToolIcons[toolIndex.index(selectedTool)])
    elif controller.A.is_pressed() and activeTool == "shovel":
        if len(supplyInventory) > 1:
            supplyMenuSprites[supplyInventory.index(activeSupply)].set_border(1, 1)
            activeSupply = supplyInventory[(supplyInventory.index(activeSupply) + len(supplyInventory) - 1) % len(supplyInventory)]
            supplyMenuSprites[supplyInventory.index(activeSupply)].set_border(1, 5)
    else:
        animation.set_action(playerSprite, ActionKind.WalkLeft)
        playerFacing = "left"
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def saveGame():
    blockSettings.write_number("gameStepCount", gameStepCount)
    blockSettings.write_number_array("timedLocations", timedLocations)
    blockSettings.write_number_array("locationTimers", locationTimers)
    blockSettings.write_number_array("timedTypes", timedTypes)
    blockSettings.write_number_array("modifiedLocations", modifiedLocations)
    blockSettings.write_number_array("locationTypes", locationTypes)
    saveInventory()

def on_right_pressed():
    global selectedTool, activeSupply, playerFacing
    if controller.B.is_pressed():
        if len(toolInventory) > 1:
            menuSprites[toolInventory.index(selectedTool)].set_image(toolIcons[toolIndex.index(selectedTool)])
            selectedTool = toolInventory[(toolInventory.index(selectedTool) + 1) % len(toolInventory)]
            menuSprites[toolInventory.index(selectedTool)].set_image(activeToolIcons[toolIndex.index(selectedTool)])
    elif controller.A.is_pressed() and activeTool == "shovel":
        if len(supplyInventory) > 1:
            supplyMenuSprites[supplyInventory.index(activeSupply)].set_border(1, 1)
            activeSupply = supplyInventory[(supplyInventory.index(activeSupply) + len(supplyInventory) + 1) % len(supplyInventory)]
            supplyMenuSprites[supplyInventory.index(activeSupply)].set_border(1, 5)
    else:
        animation.set_action(playerSprite, ActionKind.WalkRight)
        playerFacing = "right"
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_b_pressed():
    controller.move_sprite(playerSprite, 0, 0)
    showToolMenu()
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def savePlayerInfo():
    blockSettings.write_number("health", info.life())
    blockSettings.write_number("score", info.score())
    blockSettings.write_number("playerX", playerSprite.x)
    blockSettings.write_number("playerY", playerSprite.y)
    blockSettings.write_number("gameStepCount", gameStepCount)
    blockSettings.write_string("activeTool", activeTool)
def getPxDistTo(sprite1: Sprite, sprite22: Sprite):
    return Math.sqrt((sprite1.x - sprite22.x) * (sprite1.x - sprite22.x) + (sprite1.y - sprite22.y) * (sprite1.y - sprite22.y))
def setEventTimer(name: str, gameSteps: number):
    if eventTimerNames.index(name) >= 0:
        eventTimers[eventTimerNames.index(name)] = gameStepCount + gameSteps
    else:
        eventTimerNames.append(name)
        eventTimers.append(gameStepCount + gameSteps)
def hasTimerEnded(name2: str):
    return eventTimerNames.index(name2) < 0

def on_overlap_tile8(sprite9, location8):
    if activeTool == "shovel":
        if hasTimerEnded("food prompt"):
            if not (blockSettings.exists("hasPlanted")):
                tiles.place_on_tile(helperSprite, location8)
                helperSprite.say_text("Hold A to open planting menu", 2000, False)
            elif not (blockSettings.exists("hasBoughtFood")):
                playerSprite.say_text("I could by more to plant in town", 2000, True)
            setEventTimer("food prompt", 50)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile
    """),
    on_overlap_tile8)

def chopTree(col: number, row: number):
    global wood
    tiles.set_tile_at(tiles.get_tile_location(col, row),
        assets.tile("""
            myTile2
        """))
    tiles.set_wall_at(tiles.get_tile_location(col, row), False)
    timedLocations.append(col * 100 + row)
    locationTimers.append(gameStepCount + 6000)
    timedTypes.append(2)
    wood += 5
    saveGame()

def on_down_pressed():
    global playerFacing
    if controller.A.is_pressed() and activeTool == "shovel":
        pass
    elif not (controller.B.is_pressed()):
        if not (controller.left.is_pressed() or controller.right.is_pressed()):
            animation.set_action(playerSprite, ActionKind.WalkDown)
            playerFacing = "down"
    else:
        pass
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def saveInventory():
    blockSettings.write_number("wood", wood)
    blockSettings.write_number("cashMoney", cashMoney)
    blockSettings.write_number_array("foodInventory", supplyInvCount)
    savePlayerInfo()

def on_down_released():
    global playerFacing
    if not (controller.B.is_pressed()):
        if controller.up.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkUp)
            playerFacing = "up"
        elif controller.left.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkLeft)
            playerFacing = "left"
        elif controller.right.is_pressed():
            animation.set_action(playerSprite, ActionKind.WalkRight)
            playerFacing = "right"
controller.down.on_event(ControllerButtonEvent.RELEASED, on_down_released)

def hideToolMenu():
    global activeTool
    index5 = 0
    while index5 <= len(menuSprites) - 1:
        sprites.destroy(menuSprites[index5])
        index5 += 1
    index6 = 0
    while index6 <= len(textSprites) - 1:
        sprites.destroy(textSprites[index6])
        index6 += 1
    activeTool = selectedTool
    toolSprite.set_image(toolIcons[toolIndex.index(selectedTool)])
    toolSprite.set_position(scene.camera_property(CameraProperty.X),
        scene.camera_property(CameraProperty.BOTTOM) - 8)
    sprites.destroy(infoBgSprite)
anim: animation.Animation = None
infoBgSprite: Sprite = None
textSprites: List[TextSprite] = []
menuSprite: Sprite = None
selectedTool = ""
menuSprites: List[Sprite] = []
eventTimerNames: List[str] = []
eventTimers: List[number] = []
activeToolIcons: List[Image] = []
yesnoAnswer = False
toolIndex: List[str] = []
toolIcons: List[Image] = []
wood = 0
row2 = 0
col2 = 0
timedTypes: List[number] = []
toolInventory: List[str] = []
snake: Sprite = None
maxEnemies = 0
enemyList: List[Sprite] = []
cashMoney = 0
answer = 0
shopIsOpen = False
tileIndex: List[Image] = []
locationTypes: List[number] = []
modifiedLocations: List[number] = []
timedLocations: List[number] = []
locationTimers: List[number] = []
gameStepCount = 0
activeSupply = ""
supplyIndex: List[str] = []
supplyIcons: List[Image] = []
supplyInvCount: List[number] = []
textSprite: TextSprite = None
supplyInventory: List[str] = []
supplyMenuSprites: List[TextSprite] = []
activeTool = ""
toolSprite: Sprite = None
playerFacing = ""
playerSprite: Sprite = None
fire: Sprite = None
blacksmith: Sprite = None
helperSprite: Sprite = None
farmer: Sprite = None
blockSettings.clear()
tiles.set_current_tilemap(tilemap("""
    level2
"""))
home = sprites.create(assets.image("""
    myImage
"""), SpriteKind.structure)
tiles.place_on_tile(home, tiles.get_tile_location(21, 83))
farmer = sprites.create(img("""
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
    """),
    SpriteKind.npc)
tiles.place_on_tile(farmer, tiles.get_tile_location(20, 22))
farmer.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
helperSprite = sprites.create(img("""
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
    """),
    SpriteKind.npc)
blacksmith = sprites.create(img("""
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
    """),
    SpriteKind.npc)
tiles.place_on_tile(blacksmith, tiles.get_tile_location(17, 26))
blacksmith.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
fire = sprites.create(img("""
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
    """),
    SpriteKind.player)
playerSprite = sprites.create(img("""
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
    """),
    SpriteKind.player)
playerFacing = "down"
tiles.place_on_tile(playerSprite, tiles.get_tile_location(26, 85))
controller.move_sprite(playerSprite, 50, 50)
scene.camera_follow_sprite(playerSprite)
setupCharacterAnim()
toolSprite = sprites.create(assets.image("""
        hand icon inactive
    """),
    SpriteKind.Menu)
toolSprite.set_flag(SpriteFlag.GHOST_THROUGH_WALLS, True)
initGameData()
if blockSettings.exists("gameStepCount"):
    if game.ask("Load previous save?"):
        loadSave()
else:
    pass

def on_update_interval():
    global gameStepCount
    gameStepCount += 1
    playBeginning()
    index7 = 0
    while index7 <= len(locationTimers) - 1:
        if gameStepCount >= locationTimers[index7]:
            if timedTypes[index7] == 4:
                tiles.set_tile_at(tiles.get_tile_location(Math.idiv(timedLocations[index7], 100),
                        timedLocations[index7] % 100),
                    assets.tile("""
                        myTile5
                    """))
                modifiedLocations.append(timedLocations[index7])
                locationTypes.append(5)
                locationTimers.remove_at(index7)
                timedTypes.remove_at(index7)
                timedLocations.remove_at(index7)
                index7 += -1
                saveGame()
            elif timedTypes[index7] == 2:
                tiles.set_tile_at(tiles.get_tile_location(Math.idiv(timedLocations[index7], 100),
                        timedLocations[index7] % 100),
                    assets.tile("""
                        myTile1
                    """))
                locationTimers.remove_at(index7)
                timedTypes.remove_at(index7)
                timedLocations.remove_at(index7)
                index7 += -1
                saveGame()
        index7 += 1
    index8 = 0
    while index8 <= len(eventTimers) - 1:
        if gameStepCount >= eventTimers[index8]:
            eventTimerNames.remove_at(index8)
            eventTimers.remove_at(index8)
        index8 += 1
game.on_update_interval(100, on_update_interval)

def on_on_update():
    if playerSprite.vx == 0 and (playerSprite.vy == 0 and not (controller.A.is_pressed())):
        animation.stop_animation(animation.AnimationTypes.ALL, playerSprite)
    if not (controller.B.is_pressed()):
        toolSprite.set_position(scene.camera_property(CameraProperty.X),
            scene.camera_property(CameraProperty.BOTTOM) - 8)
    index9 = 0
    while index9 <= len(enemyList) - 1:
        if getPxDistTo(playerSprite, enemyList[index9]) > 180:
            sprites.destroy(enemyList.remove_at(index9))
            index9 += -1
            playerSprite.say_text("I think I got away", 1000, False)
        index9 += 1
game.on_update(on_on_update)
