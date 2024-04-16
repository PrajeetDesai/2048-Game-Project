# Structuur

index.html \
styles.css \
index.js \
/js/Game.js \
/js/Board.js \
/js/Tile.js \
/js/Handler.js


## Index.js
is waar de game start. Verzamel hier in de klassen en keyHandler.
```javascript
window.onload = () => {}
```

## Game.js
Heeft logika over de game zelf. \
**Variabelen:**
```javascript
this.size = 4 // breedte van grid.
```

**Functies:**
```javascript
startGame() // zet de eerste 2 velden. 
drawUpdate() // update de game.
```
## Board.js *extends Game*
Bevat alle functies met betrekking tot het bord.
```javascript
grid() // maakt een grid aan
getBoard() // vraag huidige bord op
```

## Tile.js *extends Board*
Bevat alle functies voor tegels\
**Variabelen:**
```javascript
this.tileValue = 2 // startwaarde tegel
```
**Functies:**
```javascript
isValid(x,y) // check of een tegel leeg is
random() // return een willekeurige tegel op een leeg veld
get()
set(x,y)
clear(x,y)
hasEmpty(row, col, toCheckRow, toCheckCol) // check of tegel ernaast leeg is
hasSameValue(row, col, toCheckRow, toCheckCol) // check of tegel ernaast dezelfde waarde heeft
```








