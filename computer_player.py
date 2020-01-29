def get_box_state(game,x,y):
    return game.board.get_box(x,y).get_state()

def make_tic_tac_toe_move(game, runde):
    if game.go_on_automatically == True:
        # check if computer could win
        for y in range(game.spielfeldbreite):
            for x in range(game.spielfeldhoehe):
                if get_box_state(game, x, y) == None:
                    if game.get_win_boxes(x,y,1) != False:
                        return x*game.spielfeldbreite + y
        # check if player could win and stop him
        for y in range(game.spielfeldbreite):
            for x in range(game.spielfeldhoehe):
                if get_box_state(game, x, y) == None:
                    if game.get_win_boxes(x,y,0) != False:
                        return x*game.spielfeldbreite + y
        # go through boxes to find an empty
        for y in range(game.spielfeldbreite):
            for x in range(game.spielfeldhoehe):
                if get_box_state(game,x,y) == None:
                    return x*game.spielfeldbreite + y

    elif runde == 0:
        # Computer fängt an und setzt in eine Ecke
        game.weg = "My way"
        return 2
    elif runde == 1:
        if get_box_state(game,0,0) == 0 or get_box_state(game,0,2) == 0 or get_box_state(game,2,0) == 0 or get_box_state(game,2,2) == 0:
            # Ecke -> Mitte
            game.weg = "Ecke"
            return 4
        elif get_box_state(game,1,2) == 0 or get_box_state(game,2,1) == 0:
            # Rand -> Ecke daneben
            game.weg = "Rand unten"
            return 8
        elif get_box_state(game,1,0) == 0 or get_box_state(game,0,1) == 0:
            # Rand -> andere Ecke
            game.weg = "Rand oben"
            return 0
        elif get_box_state(game,1,1) == 0:
            # Mitte -> Ecke
            game.weg = "Mitte"
            return 0
    elif runde == 2:
        if game.weg == "My way":
            if get_box_state(game,0,0) == 0:
                game.r2 = "My0"
                return 8
            if get_box_state(game,0,1) == 0:
                game.r2 = "My1"
                return 8
            if get_box_state(game,1,0) == 0:
                game.r2 = "My3"
                return 8
            if get_box_state(game,1,1) == 0:
                game.go_on_automatically = True
                return 6
            if get_box_state(game,1,2) == 0:
                game.r2 = "My5"
                return 0
            if get_box_state(game,2,0) == 0:
                game.r2 = "My6"
                return 8
            if get_box_state(game,2,1) == 0:
                game.r2 = "My7"
                return 0
            if get_box_state(game,2,2) == 0:
                game.r2 = "My8"
                return 0
    elif runde == 3:
        if game.weg == "Ecke":
            if get_box_state(game,0,0) == 0:
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 2
                if get_box_state(game,0,2) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 6
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 2
                if get_box_state(game,2,0) == 0:
                    game.go_on_automatically = True
                    return 3
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 6
                if get_box_state(game,2,2) == 0:
                    game.go_on_automatically = True
                    return 1
            elif get_box_state(game,0,2) == 0:
                if get_box_state(game,0,0) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,0,1) == 0:
                    return 0
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 0
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 8
                if get_box_state(game,2,0) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 8
                if get_box_state(game,2,2) == 0:
                    game.go_on_automatically = True
                    return 5
            elif get_box_state(game,2,0) == 0:
                if get_box_state(game,0,0) == 0:
                    game.go_on_automatically = True
                    return 3
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 0
                if get_box_state(game,0,2) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 0
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 8
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 8
                if get_box_state(game,2,2) == 0:
                    game.go_on_automatically = True
                    return 7
            elif get_box_state(game,2,2) == 0:
                if get_box_state(game,0,0) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 2
                if get_box_state(game,0,2) == 0:
                    game.go_on_automatically = True
                    return 5
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 6
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 2
                if get_box_state(game,2,0) == 0:
                    game.go_on_automatically = True
                    return 7
                if get_box_state(game,2,1) == 0:
                    game.r2 = "E87"
                    return 6
        elif game.weg == "Rand unten":
            if get_box_state(game,1,2) == 0:
                if get_box_state(game,0,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,0,2) == 0:
                    game.r2 = "Ru52"
                    return 6
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,1,1) == 0:
                    game.go_on_automatically = True
                    return 3
                if get_box_state(game,2,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 4
            elif get_box_state(game,2,1) == 0:
                if get_box_state(game,0,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,0,2) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,1,1) == 0:
                    game.go_on_automatically = True
                    return 1
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,0) == 0:
                    game.r2 = "Ru76"
                    return 2
        elif game.weg == "Rand oben":
            if get_box_state(game,0,1) == 0:
                if get_box_state(game,0,2) == 0:
                    game.r2 = "Ro12"
                    return 6
                if get_box_state(game,1,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,1,1) == 0:
                    game.go_on_automatically = True
                    return 7
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,0) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,2) == 0:
                    game.go_on_automatically = True
                    return 4
            elif get_box_state(game,1,0) == 0:
                if get_box_state(game,0,1) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,0,2) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,1,1) == 0:
                    game.go_on_automatically = True
                    return 5
                if get_box_state(game,1,2) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,0) == 0:
                    game.r2 = "Ro36"
                    return 2
                if get_box_state(game,2,1) == 0:
                    game.go_on_automatically = True
                    return 4
                if get_box_state(game,2,2) == 0:
                    game.go_on_automatically = True
                    return 4
        elif game.weg == "Mitte":
            if get_box_state(game,0,1) == 0:
                game.go_on_automatically = True
                return 7
            if get_box_state(game,0,2) == 0:
                game.go_on_automatically = True
                return 6
            if get_box_state(game,1,0) == 0:
                game.go_on_automatically = True
                return 5
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 3
            if get_box_state(game,2,0) == 0:
                game.go_on_automatically = True
                return 2
            if get_box_state(game,2,1) == 0:
                game.go_on_automatically = True
                return 1
            if get_box_state(game,2,2) == 0:
                game.go_on_automatically = True
                return 6
    elif runde == 4:
        if game.r2 == "My0":
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 6
            else:
                game.go_on_automatically = True
                return 5
        elif game.r2 == "My1":
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 6
            else:
                game.go_on_automatically = True
                return 5
        elif game.r2 == "My3":
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 6
            else:
                game.go_on_automatically = True
                return 5
        elif game.r2 == "My5":
            if get_box_state(game,0,1) == 0:
                game.go_on_automatically = True
                return 6
            else:
                game.go_on_automatically = True
                return 1
        elif game.r2 == "My6":
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 0
            else:
                game.go_on_automatically = True
                return 5
        elif game.r2 == "My7":
            if get_box_state(game,0,1) == 0:
                game.go_on_automatically = True
                return 8
            else:
                game.go_on_automatically = True
                return 1
        elif game.r2 == "My8":
            if get_box_state(game,0,1) == 0:
                game.go_on_automatically = True
                return 6
            else:
                game.go_on_automatically = True
                return 1
    elif runde == 5:
        if game.r2 == "Ru52":
            if get_box_state(game,2,1) == 0:
                game.go_on_automatically = True
                return 0
            else:
                game.go_on_automatically = True
                return 7
        elif game.r2 == "Ru76":
            if get_box_state(game,1,2) == 0:
                game.go_on_automatically = True
                return 0
            else:
                game.go_on_automatically = True
                return 5
        elif game.r2 == "Ro12":
            if get_box_state(game,1,0) == 0:
                game.go_on_automatically = True
                return 8
            else:
                game.go_on_automatically = True
                return 3
        elif game.r2 == "Ro36":
            if get_box_state(game,0,1) == 0:
                game.go_on_automatically = True
                return 8
            else:
                game.go_on_automatically = True
                return 1
        elif game.r2 == "E87":
            if get_box_state(game,0,2) == 0:
                game.go_on_automatically = True
                return 2
            else:
                game.go_on_automatically = True
                return 3

    print("upsiiis",runde,game.go_on_automatically,game.weg)
    return False