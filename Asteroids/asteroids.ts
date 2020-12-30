// FIT2102 2019 Assignment 1
// https://docs.google.com/document/d/1Gr-M6LTU-tfm4yabqZWJYg-zTjEVqHKKTCvePGCYsUA/edit?usp=sharing

function asteroids() {
  //Game Implementatation:
  // This game can be played using the arrow keys and space bar. The arrow keys are used
  // to control the ship and the space bar is used to shoot the asteroids. The ship can 
  // be rotated using the left/ right arrow keys and move forward using the up and down
  // arrow keys. The ship shoots bullets when the space bar is pressed. In order to win the game,
  // all the asteroids need to be destroyed. The player loses the game when he/she is hit
  // more than 3 times. The score is located on the top left of the screen.The green circles on the 
  // top right corner indicate the players life.
  // When the game is over or when the player wins the game, a restart button can be 
  // pressed to reload the page. 

  // --- ADDITIONAL ---
  // Additional things added to the game:
  // - Ship can glide when arrow key is pressed
  // - Player has 3 lives (signified by the three green dots at the top right of the screen)
  // - Asteroids can be split into two depending if the asteroids are big enough
  // - Asteroids are generated and added to a list recursively. The size and coordinates of the 
  //   asteroids are generated randomly. The number of asteroids present in the game are
  //   also generated randomly (from 10-15 asteroids)
  // - Score for the player is calculated
  // - There is a restart button when the game ends (Idea gotten from W3Schools.com on how to reload the page)


  const svg = document.getElementById("canvas")!,
  keydown = Observable.fromEvent<KeyboardEvent>(document, 'keydown'),
  keyup = Observable.fromEvent<KeyboardEvent>(document, 'keyup');

  // function that converts degree to radian
  const toRad=(angle:number)=> angle*Math.PI/180;
  
  // The reason why I made these currying functions was because it is much easier to see when I code.
  // The attributes are displayed better when using a curried function since it has so many parameters.
  // this function uses the concept of currying learnt in lectures to create a bullet. Its a reusable function as
  // you can use this function to create bullet by passing the attributes into the parameters. It
  // makes the code look cleaner
  const createBullet = (elem:Elem)=> (x:number) => (y:number) => (height:number) => (width:number) => (fill:string) => {return new Elem(svg,'rect')
  .attr('x',x)
  .attr('y',y)
  .attr('height',height)
  .attr('width',width)
  .attr('fill',fill)
  }

  // this function uses the concept of currying learnt in lectures to create an asteroid. Its a reusable function as
  // you can use this function to create bullet by passing the attributes into the parameters. It
  // makes the code look less congested
  const createAsteroid = (elem:Elem)=> (cx:number) => (cy:number) => (r:number) => (fill:string) => (gotHit:string)=> (stroke:string)=>{return new Elem(svg,'circle')
  .attr('cx',cx)
  .attr('cy',cy)
  .attr('r',r)
  .attr('fill',fill)
  .attr('gotHit',gotHit)
  .attr('stroke',stroke)
  }

  // this function uses currying to create a text element. This makes the code look less congested.
  const createText = (elem:Elem) => (x:number) => (y:number) => (style:string) => (id:string) => {return new Elem(svg,'text')
  .attr('x',x)
  .attr('y',y)
  .attr('style',style)
  .attr('id',id)
}

//this function generates random numbers from 1 till N
const generateRandom=(n:number) => Math.floor(Math.random()*n)+1;

//this function generates random numbers from a number to N
const generateRandomAbove=(n:number,lowerNum:number) => Math.floor(Math.random()*n)+lowerNum;

//this function picks a random number from 2 given numbers
function pickPos(n1:number,n2:number):number {
  let rand = Math.floor(Math.random()*2)+1
  return rand == 1 ? n1 : n2
}

// makes the asteroids different colours
function getColour(){
  let colourList = ['grey','silver']
  let rand =  Math.floor(Math.random()*2)
  return colourList[rand]
}

// this function generates a random number from 1-200 or 400-600
function randomCoord():number{
  return pickPos(generateRandom(200),generateRandomAbove(200,400))
}

// this function generates a random size
function randomSize():number{
  return generateRandomAbove(20,20)
}

//initializes the asteroid list
let asteroidsList: Elem[]=[];

//this function uses the concept of recursion and a ternary operator to recursively create asteroids and 
// add them to a list. This is good for flexibility of the game. If a person would want to make
// the game more challenging, more asteroids being added to the game can easily be done. This also
// prevents duplication of code as the function can be reused whenever asteroids need to be created
function createAsteroids(number:number): Elem[]{
  return number == 0 ? [] : createAsteroids(number-1).concat([createAsteroid(new Elem(svg,'circle'))(randomCoord())(randomCoord())(randomSize())(getColour())('false')('white')])
}

// make a group for the spaceship and a transform to move it and rotate it
  // to animate the spaceship you will update the transform property
    //.attr("transform","translate("+x.toString()+" "+y.toString()+") rotate("+angle.toString()+")")  
    let g = new Elem(svg,'g')
    .attr("transform","translate(300 300) rotate(0)")
    

  // create a polygon shape for the space ship as a child of the transform group
  let ship = new Elem(svg, 'polygon', g.elem) 
    .attr("points","-15,20 15,20 0,-20")
    .attr("style","fill:magenta;stroke:purple;stroke-width:1")
  

  // gets the starting coordinates of the ship by using a regular expression to only get the numbers
  // from 0-9 from the string into a list. The x and y values can then be retrieved by
  // getting the index from the lists
  let x = Number(g.attr('transform').match(/[0-9]+/g)![0]),
  y = Number(g.attr('transform').match(/[0-9]+/g)![1]),
  angle = Number(g.attr('transform').match(/[0-9]+/g)![2]);

  //global variables :
  const speed = 10,
  degree = 10;
  let isShipHit = false;
  let hasPlayerWon = false;
  let playerLife = 3;
  const glideSpeed = 0.5;

  // creates the text to be put on the html document
  const score = createText(new Elem(svg,'txt'))(80)(20)('fill:white;stroke:white;font-size:20px')('score')
  const scoreText = createText(new Elem(svg,'text'))(20)(20)('fill:white;stroke:white;font-size:20px')('scoreText')
  const gameOverText = createText(new Elem(svg,'text'))(100)(300)('fill:white;stroke:white;font-size:24px')('gameOverText')
  const lives = createText(new Elem(svg,'text'))(450)(25)('fill:white;stroke:white;font-size:20px')('lives')


  // this is the main clock of the game. It stops everything when the player has been hit 3 times or the player has
  // destroyed all the asteroids.
  const mainClock = Observable.interval(10).map(()=>({isShipHit})).map(()=> {hasPlayerWon})

  // main Observable used in the game, It stops when the player's life has run out or when the player wins the game
  let obs = Observable.interval(10).takeUntil( mainClock.filter(()=> isShipHit==true)),
  wrapAround = obs,
  shootBullet = obs,
  glide = obs;

  //To move the space ship using the arrow keys
  // ArrowUp and ArrowDown do the same things, but for convienece of the player, its used in both
  keydown
  // stops when the player life is up or 
  .takeUntil( mainClock.filter(()=> isShipHit==true || hasPlayerWon == true))
  .filter(e => e.key == "ArrowUp")
  // adds the 'fire' effect to the spaceship when arrow key is pressed
  .map(()=> ({fire: new Elem(svg,'polygon',g.elem)
              .attr("points","10,20 -10,20 0,35")
              .attr("style","fill:orange;stroke:yellow;stroke-width:3")}))

  // changes the coordinates of the ship when arrow key is pressed. This formula was taken from
  // an online source so that the ship can move in whatever direction it is facing
  .map(({fire}) => ({x2:x+= Math.sin(toRad(angle))*speed,y2:y-=Math.cos(toRad(angle))*speed,angle:angle,fire:fire}))
  .subscribe(({x2,y2,angle,fire})=> {g.attr("transform","translate("+x2.toString()+" "+y2.toString()+") rotate("+angle.toString()+")"),
                              // causes ship to glide after pressing the arrow key
                              glide
                                .takeUntil(Observable.interval(500))
                                .map(({})=>({x2:x+= Math.sin(toRad(angle))*glideSpeed,y2:y-=Math.cos(toRad(angle))*glideSpeed}))
                                .subscribe(({x2,y2})=>{x = x2,g.attr("transform","translate("+x2.toString()+" "+y2.toString()+") rotate("+angle.toString()+")"),
                                        // updates the global x and y value
                                          x += Math.sin(toRad(angle))*glideSpeed, y -=Math.cos(toRad(angle))*glideSpeed
                                      })

                              // fire effect is removed when key is let go
                              keyup.map(()=>fire.elem.remove())
                                  .subscribe(()=>{})}
                              )

  keydown
  .takeUntil( mainClock.filter(()=> isShipHit==true || hasPlayerWon == true))
  .filter(e => e.key == "ArrowDown")
  // adds the 'fire' effect to the spaceship when arrow key is pressed
  .map(()=> ({fire: new Elem(svg,'polygon',g.elem)
              .attr("points","10,20 -10,20 0,35")
              .attr("style","fill:orange;stroke:yellow;stroke-width:3")}))

  // changes the coordinates of the ship when arrow key is pressed. This formula was taken from
  // an online source so that the ship can move in whatever direction it is facing
  .map(({fire}) => ({x2:x+= Math.sin(toRad(angle))*speed,y2:y-=Math.cos(toRad(angle))*speed,angle:angle,fire:fire}))
  .subscribe(({x2,y2,angle,fire})=> {g.attr("transform","translate("+x2.toString()+" "+y2.toString()+") rotate("+angle.toString()+")"),
                                glide
                                .takeUntil(Observable.interval(500))
                                .map(({})=>({x2:x+= Math.sin(toRad(angle))*glideSpeed,y2:y-=Math.cos(toRad(angle))*glideSpeed}))
                                .subscribe(({x2,y2})=>{x = x2,g.attr("transform","translate("+x2.toString()+" "+y2.toString()+") rotate("+angle.toString()+")"),
                                        // updates the global x and y value
                                          x += Math.sin(toRad(angle))*glideSpeed, y -=Math.cos(toRad(angle))*glideSpeed
                                      })

                            // fire effect is removed when key is let go
                              keyup.map(()=>fire.elem.remove())
                              .subscribe(()=>{})}
              )  

  // //just prints stuff !!!
  // keydown
  // .filter(e => e.key == "ArrowDown" || e.key == "ArrowUp") 
  // .subscribe(()=>console.log(x,y,asteroidsList))
  
  // This observable rotates the ship to the right when the arrow key is pressed
  keydown
  .takeUntil( mainClock.filter(()=> isShipHit==true || hasPlayerWon == true))
  .filter(e => e.key == "ArrowRight")
  .map(({}) => ({x:x,y:y,angle:(angle = (angle + degree)%360)}))
  .subscribe(({x,y,angle})=> g.attr("transform","translate("+x.toString()+" "+y.toString()+") rotate("+angle.toString()+")"))

  // This observable rotates the ship to the left when the arrow key is pressed
  keydown  .takeUntil( mainClock.filter(()=> isShipHit==true || hasPlayerWon == true))
  .filter(e => e.key == "ArrowLeft")
  .map(({}) => ({x:x,y:y,angle:angle=(((angle-degree)+360)%360)}))
  .subscribe(({x,y,angle})=> g.attr("transform","translate("+x.toString()+" "+y.toString()+") rotate("+angle.toString()+")"))

  // to display the text
const gameOver:HTMLElement = document.getElementById('gameOverText')!;
const scoreDisplay:HTMLElement = document.getElementById('score')!;
const scoreDisplayText:HTMLElement = document.getElementById('scoreText')!;
const livesDisplayText:HTMLElement = document.getElementById('lives')!;

scoreDisplayText.innerHTML = "Score:"
scoreDisplay.innerHTML = "0"
livesDisplayText.innerHTML = "Lives:"

// Creates 'life' so that the player knows how many lives they have at any point in the game
// These lifes will dissapear when the player gets hit by the asteroid
const life1 = new Elem(svg,"circle")
.attr('cx',520)
.attr('cy',20)
.attr('r',10)
.attr('fill','green')
.attr('stroke','white')

const life2 = new Elem(svg,"circle")
.attr('cx',545)
.attr('cy',20)
.attr('r',10)
.attr('fill','green')
.attr('stroke','white')

const life3 = new Elem(svg,"circle")
.attr('cx',570)
.attr('cy',20)
.attr('r',10)
.attr('fill','green')
.attr('stroke','white')

//shoots a bullet
  keydown
  .filter(e => e.key == " ")
  // creates a new bullet element
  .map(() => ({bullet: createBullet(new Elem(svg,'rect'))(x)(y)(10)(5)('pink'), fixedAngle:angle}))
  .subscribe(({bullet,fixedAngle})=> {
    const a =
    shootBullet
        .takeUntil(Observable.interval(6000))
        .subscribe(()=> {
          // moves the bullet continously for 6 seconds. The angle is passed in as a parameter
          // so that the bullet is shot in the direction that the ship is currently facing
          bullet.attr('x',Number(bullet.attr('x'))+ Math.sin(toRad(fixedAngle))*1)
                .attr('y',Number(bullet.attr('y'))- Math.cos(toRad(fixedAngle))*1),

                // checks to see if the asteroids are colliding with the bullet
                // if asteroid is hit, the asteroid is checked to see if it can be broken down into 2.
                // bullet and asteroid is also removed from the game and list of asteroids
                        asteroidsList.forEach(asteroid => {if (checkAsteroidBulletCollision(asteroid,bullet)){
                          asteroid.attr('gotHit','true')
                          breakDownAsteroid(asteroid) //checks if asteroid can be broken down, then breaks it down
                          asteroidsList = asteroidsList.filter(removeAsteroidFromList) // removes asteroids that have been destroyed
                          asteroid.attr('cx',3000) // relocates position of asteroid that has been hit
                          asteroid.attr('cy',3000)

                          // removes asteroid and bullet
                          asteroid.elem.remove();
                          bullet.elem.remove()

                          // updates the players score. The score increases by 10 every time the player hits an asteroid
                          scoreDisplay.innerHTML = String(((Number(scoreDisplay.innerHTML)) + 10))


                          // if there are no more asteroids, the player has won
                          if (checkAsteroidList()){
                            hasPlayerWon = true;
                            gameOver.innerHTML = "Congratulations ! YOU HAVE WON!"
                            displayButton()
                          }
                          a();
                        }})
})})

// removes asteroids from the global list if it has already been hit by a bullet
function removeAsteroidFromList(asteroid:Elem){
  return asteroid.attr('gotHit') == 'false';
}

// checks asteroid radius 
function canAsteroidBeBroken(asteroid:Elem){
  return Number(asteroid.attr('r')) > 30
}

/**
 * This function firstly checks if an asteroid can be broken down (based on its radius). It only breaks
 * down the asteroid if it is big enough, in this case if the radius is > 30. Two new asteroids are created
 * when the bigger one is broken down.
 * @param asteroid asteroid to check if it can be broken down
 */
function breakDownAsteroid(asteroid:Elem){
  if (canAsteroidBeBroken(asteroid) == true){
    // creates two new asteroids
    const newAsteroid1 = createAsteroid(new Elem(svg,'circle'))(Number(asteroid.attr('cx')))(Number(asteroid.attr('cy')))(Number(asteroid.attr('r'))/2)('gainsboro')('false')('white'),
    newAsteroid2 = createAsteroid(new Elem(svg,'circle'))(Number(asteroid.attr('cx')))(Number(asteroid.attr('cy')))(Number(asteroid.attr('r'))/2)('gainsboro')('false')('white');

    // adds the new asteroids to the list
    asteroidsList.push(newAsteroid1)
    asteroidsList.push(newAsteroid2)

    // gives the asteroids movement and checks if asteroids have collided with the ship
    randomizeAsteroidMovement(newAsteroid1)
    randomizeAsteroidMovement(newAsteroid2)
    checkShipCollision(newAsteroid1)
    checkShipCollision(newAsteroid2)
  }
}

/**
 * This function moves the asteroids and randomizes the movement of the asteroid. The movement
 * of the asteroid is achieved using an observable. Firstly, to randomize the movement, two angles are
 * generated. The x and y coordinates are then changed accordingly.
 * @param asteroid asteroid to move
 */
function randomizeAsteroidMovement(asteroid:Elem){
  let asteroidMovement = Observable.interval(50).takeUntil( mainClock.filter(()=> isShipHit==true || hasPlayerWon == true))
     let angleForX = generateRandom(360);
     let angleForY = generateRandom(360)
  asteroidMovement
  // the angles are generated randomly
    .map(()=> ({x:Number(asteroid.attr('cx'))+Math.sin(toRad(angleForX)), 
                y:Number(asteroid.attr('cy'))-Math.cos(toRad(angleForY)),
                r:asteroid.attr('r')}))
  // susbscribe updates the x and y values of the asteroid
    .subscribe(({x,y})=> asteroid.attr('cx',x)
                                .attr('cy',y))
  
  // This portion of code makes sure the asteroids wrap around the edges so they dont 
  // go out of the frame, and if they do, their x or y coordinates are reset.
    asteroidMovement
    .filter(() => (Number(asteroid.attr('cx')) >(600+Number(asteroid.attr('r')))) && (Number(asteroid.attr('cx')) < (600+Number(asteroid.attr('r'))+5)))
    .subscribe(()=>asteroid.attr('cx',0));

    asteroidMovement
    .filter(() => Number(asteroid.attr('cx')) < 0 )
    .subscribe(()=>asteroid.attr('cx',(600+Number(asteroid.attr('r')))));

    asteroidMovement
    .filter(() => (Number(asteroid.attr('cy')) > (600+Number(asteroid.attr('r')))) && (Number(asteroid.attr('cy')) < (600+Number(asteroid.attr('r'))+5)))
    .subscribe(()=>asteroid.attr('cy',0));

    asteroidMovement
    .filter(() => Number(asteroid.attr('cy')) < 0 )
    .subscribe(()=>asteroid.attr('cy',(600+Number(asteroid.attr('r')))));
    
}

/**
 * This function gets the distance between two points. The mathematical formula for this function
 * was found online. It gets the distance between two points, for example: Point1(x1,y1) and
 * Point2(x2,y2)
 * @param point_x1 : x coordinate of first point
 * @param point_x2 : x coordinate of second point
 * @param point_y1 : y coordinate of first point
 * @param point_y2 : y coordinate of second point
 */
function getDistance(point_x1:number,point_x2:number,point_y1:number,point_y2:number):number{
  return Math.sqrt(Math.pow(point_x2 - point_x1, 2) + Math.pow(point_y2 - point_y1, 2))
}

// This function is to check whether the asteroid list is empty
function checkAsteroidList(){
  return asteroidsList.length == 0
}

//This function is to display the restart button, which just reloads the page
function displayButton(){
const restartGameButton = new Elem(svg,'rect').attr('x',250).attr('y',325).attr('width',75).attr('height',50).attr('fill',"#ffffff00").attr('stroke','yellow');
  restartGameButton.observe<MouseEvent>('mousedown').subscribe(()=>location.reload())
  const restartText = new Elem(svg,'text').attr('x',260).attr('y',350).attr('style','fill:white;stroke:white;font-size:15px').attr('id','restartText')
const restart:HTMLElement = document.getElementById('restartText')!;
restart.innerHTML = "Restart"
}

// this function removes the life from the view of the player when they have been hit
function removeLife(){
  let remove = obs
  remove
  .filter(()=>playerLife == 2)
  .subscribe(()=>life1.elem.remove())

  remove
  .filter(()=>playerLife == 1)
  .subscribe(()=>life2.elem.remove())

  remove
  .filter(()=>playerLife == 0)
  .subscribe(()=>life3.elem.remove())

}

/**
 * This function checks whether the ship has collided with the asteroid. It uses an obeservable
 * called collision. If the player has been hit more than 3 times, the game is over
 * @param asteroid asteroid to check for collision with the ship
 */
function checkShipCollision(asteroid:Elem){
  let collision = obs
  collision
  // checks if there is a collision between the ship and asteroid
  .filter(()=>getDistance(x,Number(asteroid.attr('cx')) ,y , Number(asteroid.attr('cy'))) < 15+Number(asteroid.attr('r')))

  // if ship is hit by the asteroid, the players life gets deducted
  .map(()=>(playerLife -= 1))
  .map(()=>removeLife())

  // if the players life is 0, the game is over
  .filter(()=> playerLife == 0)
  .map(()=>(isShipHit=true))
  .subscribe(()=>{printLoseMessage()})

  // when the ship collides with the asteroid, the ship gets put back at the starting position coordinates
  collision
  .filter(()=>getDistance(x,Number(asteroid.attr('cx')) ,y , Number(asteroid.attr('cy'))) < 15+Number(asteroid.attr('r')))
  .subscribe(()=> {x = 300,y=300});


}

// this functions prints a message when the player gets hit by the asteroid. It also displays
// the restart game button
function printLoseMessage(){
  const playerLost = new Elem(svg,'text').attr('x',75).attr('y',300).attr('style','fill:white;stroke:white;font-size:20px').attr('id','playerLost')
  const playerLostMsg:HTMLElement = document.getElementById('playerLost')!;
  playerLostMsg.innerHTML = "Your ship got hit by an asteroid! The game is over!"
  const playerLost2 = new Elem(svg,'text').attr('x',100).attr('y',320).attr('style','fill:white;stroke:white;font-size:20px').attr('id','playerLost2')
  const playerLostMsg2:HTMLElement = document.getElementById('playerLost2')!;
  playerLostMsg2.innerHTML = "Click the button below to restart the game!"

  displayButton()
}

/**
 * This function checks whether the bullet hit the asteroid. It gets the distance between the bullet and asteroid
 * then checks if it is less than the radius of the asteroid to see if the coordinates are overlapping.
 * @param asteroid asteroid to check for collision
 * @param bullet generated bullet when player presses the space bar
 */
function checkAsteroidBulletCollision(asteroid:Elem,bullet:Elem):boolean{
  return getDistance(Number(bullet.attr('x')),Number(asteroid.attr('cx')) ,Number(bullet.attr('y')) , Number(asteroid.attr('cy'))) < Number(asteroid.attr('r'))
}

// This function does the wrapping. It puts the ship the ship back at a certain coordinate
// when the ship goes off the canvas. This eases the gameplay so that the ship will go off the page
// and appear on the other side.
function wrap(){
  // wraps around the canvas
  wrapAround
    .filter(() =>x > 620)
    .subscribe(()=> x = 20);

  wrapAround
    .filter(() =>x < 0)
    .subscribe(()=> x = 620);

  wrapAround
    .filter(() =>y < 0)
    .subscribe(()=> y = 620);

  wrapAround
    .filter(() =>y > 620)
    .subscribe(()=> y = 20);
}

// runs all the functions 
wrap()
asteroidsList= createAsteroids(generateRandomAbove(10,5));
asteroidsList.forEach(element=>randomizeAsteroidMovement(element))
asteroidsList.forEach(element=>checkShipCollision(element))

}
// the following simply runs your asteroids function on window load.  Make sure to leave it in place.
if (typeof window != 'undefined')
  window.onload = ()=>{
    asteroids();
  }