"use strict";
function asteroids() {
    const svg = document.getElementById("canvas"), keydown = Observable.fromEvent(document, 'keydown'), keyup = Observable.fromEvent(document, 'keyup');
    const toRad = (angle) => angle * Math.PI / 180;
    const createBullet = (elem) => (x) => (y) => (height) => (width) => (fill) => {
        return new Elem(svg, 'rect')
            .attr('x', x)
            .attr('y', y)
            .attr('height', height)
            .attr('width', width)
            .attr('fill', fill);
    };
    const createAsteroid = (elem) => (cx) => (cy) => (r) => (fill) => (gotHit) => (stroke) => {
        return new Elem(svg, 'circle')
            .attr('cx', cx)
            .attr('cy', cy)
            .attr('r', r)
            .attr('fill', fill)
            .attr('gotHit', gotHit)
            .attr('stroke', stroke);
    };
    const createText = (elem) => (x) => (y) => (style) => (id) => {
        return new Elem(svg, 'text')
            .attr('x', x)
            .attr('y', y)
            .attr('style', style)
            .attr('id', id);
    };
    const generateRandom = (n) => Math.floor(Math.random() * n) + 1;
    const generateRandomAbove = (n, lowerNum) => Math.floor(Math.random() * n) + lowerNum;
    function pickPos(n1, n2) {
        let rand = Math.floor(Math.random() * 2) + 1;
        return rand == 1 ? n1 : n2;
    }
    function getColour() {
        let colourList = ['grey', 'silver'];
        let rand = Math.floor(Math.random() * 2);
        return colourList[rand];
    }
    function randomCoord() {
        return pickPos(generateRandom(200), generateRandomAbove(200, 400));
    }
    function randomSize() {
        return generateRandomAbove(20, 20);
    }
    let asteroidsList = [];
    function createAsteroids(number) {
        return number == 0 ? [] : createAsteroids(number - 1).concat([createAsteroid(new Elem(svg, 'circle'))(randomCoord())(randomCoord())(randomSize())(getColour())('false')('white')]);
    }
    let g = new Elem(svg, 'g')
        .attr("transform", "translate(300 300) rotate(0)");
    let ship = new Elem(svg, 'polygon', g.elem)
        .attr("points", "-15,20 15,20 0,-20")
        .attr("style", "fill:magenta;stroke:purple;stroke-width:1");
    let x = Number(g.attr('transform').match(/[0-9]+/g)[0]), y = Number(g.attr('transform').match(/[0-9]+/g)[1]), angle = Number(g.attr('transform').match(/[0-9]+/g)[2]);
    const speed = 10, degree = 10;
    let isShipHit = false;
    let hasPlayerWon = false;
    let playerLife = 3;
    const glideSpeed = 0.5;
    const score = createText(new Elem(svg, 'txt'))(80)(20)('fill:white;stroke:white;font-size:20px')('score');
    const scoreText = createText(new Elem(svg, 'text'))(20)(20)('fill:white;stroke:white;font-size:20px')('scoreText');
    const gameOverText = createText(new Elem(svg, 'text'))(100)(300)('fill:white;stroke:white;font-size:24px')('gameOverText');
    const lives = createText(new Elem(svg, 'text'))(450)(25)('fill:white;stroke:white;font-size:20px')('lives');
    const mainClock = Observable.interval(10).map(() => ({ isShipHit })).map(() => { hasPlayerWon; });
    let obs = Observable.interval(10).takeUntil(mainClock.filter(() => isShipHit == true)), wrapAround = obs, shootBullet = obs, glide = obs;
    keydown
        .takeUntil(mainClock.filter(() => isShipHit == true || hasPlayerWon == true))
        .filter(e => e.key == "ArrowUp")
        .map(() => ({ fire: new Elem(svg, 'polygon', g.elem)
            .attr("points", "10,20 -10,20 0,35")
            .attr("style", "fill:orange;stroke:yellow;stroke-width:3") }))
        .map(({ fire }) => ({ x2: x += Math.sin(toRad(angle)) * speed, y2: y -= Math.cos(toRad(angle)) * speed, angle: angle, fire: fire }))
        .subscribe(({ x2, y2, angle, fire }) => {
        g.attr("transform", "translate(" + x2.toString() + " " + y2.toString() + ") rotate(" + angle.toString() + ")"),
            glide
                .takeUntil(Observable.interval(500))
                .map(({}) => ({ x2: x += Math.sin(toRad(angle)) * glideSpeed, y2: y -= Math.cos(toRad(angle)) * glideSpeed }))
                .subscribe(({ x2, y2 }) => {
                x = x2, g.attr("transform", "translate(" + x2.toString() + " " + y2.toString() + ") rotate(" + angle.toString() + ")"),
                    x += Math.sin(toRad(angle)) * glideSpeed, y -= Math.cos(toRad(angle)) * glideSpeed;
            });
        keyup.map(() => fire.elem.remove())
            .subscribe(() => { });
    });
    keydown
        .takeUntil(mainClock.filter(() => isShipHit == true || hasPlayerWon == true))
        .filter(e => e.key == "ArrowDown")
        .map(() => ({ fire: new Elem(svg, 'polygon', g.elem)
            .attr("points", "10,20 -10,20 0,35")
            .attr("style", "fill:orange;stroke:yellow;stroke-width:3") }))
        .map(({ fire }) => ({ x2: x += Math.sin(toRad(angle)) * speed, y2: y -= Math.cos(toRad(angle)) * speed, angle: angle, fire: fire }))
        .subscribe(({ x2, y2, angle, fire }) => {
        g.attr("transform", "translate(" + x2.toString() + " " + y2.toString() + ") rotate(" + angle.toString() + ")"),
            glide
                .takeUntil(Observable.interval(500))
                .map(({}) => ({ x2: x += Math.sin(toRad(angle)) * glideSpeed, y2: y -= Math.cos(toRad(angle)) * glideSpeed }))
                .subscribe(({ x2, y2 }) => {
                x = x2, g.attr("transform", "translate(" + x2.toString() + " " + y2.toString() + ") rotate(" + angle.toString() + ")"),
                    x += Math.sin(toRad(angle)) * glideSpeed, y -= Math.cos(toRad(angle)) * glideSpeed;
            });
        keyup.map(() => fire.elem.remove())
            .subscribe(() => { });
    });
    keydown
        .takeUntil(mainClock.filter(() => isShipHit == true || hasPlayerWon == true))
        .filter(e => e.key == "ArrowRight")
        .map(({}) => ({ x: x, y: y, angle: (angle = (angle + degree) % 360) }))
        .subscribe(({ x, y, angle }) => g.attr("transform", "translate(" + x.toString() + " " + y.toString() + ") rotate(" + angle.toString() + ")"));
    keydown.takeUntil(mainClock.filter(() => isShipHit == true || hasPlayerWon == true))
        .filter(e => e.key == "ArrowLeft")
        .map(({}) => ({ x: x, y: y, angle: angle = (((angle - degree) + 360) % 360) }))
        .subscribe(({ x, y, angle }) => g.attr("transform", "translate(" + x.toString() + " " + y.toString() + ") rotate(" + angle.toString() + ")"));
    const gameOver = document.getElementById('gameOverText');
    const scoreDisplay = document.getElementById('score');
    const scoreDisplayText = document.getElementById('scoreText');
    const livesDisplayText = document.getElementById('lives');
    scoreDisplayText.innerHTML = "Score:";
    scoreDisplay.innerHTML = "0";
    livesDisplayText.innerHTML = "Lives:";
    const life1 = new Elem(svg, "circle")
        .attr('cx', 520)
        .attr('cy', 20)
        .attr('r', 10)
        .attr('fill', 'green')
        .attr('stroke', 'white');
    const life2 = new Elem(svg, "circle")
        .attr('cx', 545)
        .attr('cy', 20)
        .attr('r', 10)
        .attr('fill', 'green')
        .attr('stroke', 'white');
    const life3 = new Elem(svg, "circle")
        .attr('cx', 570)
        .attr('cy', 20)
        .attr('r', 10)
        .attr('fill', 'green')
        .attr('stroke', 'white');
    keydown
        .filter(e => e.key == " ")
        .map(() => ({ bullet: createBullet(new Elem(svg, 'rect'))(x)(y)(10)(5)('pink'), fixedAngle: angle }))
        .subscribe(({ bullet, fixedAngle }) => {
        const a = shootBullet
            .takeUntil(Observable.interval(6000))
            .subscribe(() => {
            bullet.attr('x', Number(bullet.attr('x')) + Math.sin(toRad(fixedAngle)) * 1)
                .attr('y', Number(bullet.attr('y')) - Math.cos(toRad(fixedAngle)) * 1),
                asteroidsList.forEach(asteroid => {
                    if (checkAsteroidBulletCollision(asteroid, bullet)) {
                        asteroid.attr('gotHit', 'true');
                        breakDownAsteroid(asteroid);
                        asteroidsList = asteroidsList.filter(removeAsteroidFromList);
                        asteroid.attr('cx', 3000);
                        asteroid.attr('cy', 3000);
                        asteroid.elem.remove();
                        bullet.elem.remove();
                        scoreDisplay.innerHTML = String(((Number(scoreDisplay.innerHTML)) + 10));
                        if (checkAsteroidList()) {
                            hasPlayerWon = true;
                            gameOver.innerHTML = "Congratulations ! YOU HAVE WON!";
                            displayButton();
                        }
                        a();
                    }
                });
        });
    });
    function removeAsteroidFromList(asteroid) {
        return asteroid.attr('gotHit') == 'false';
    }
    function canAsteroidBeBroken(asteroid) {
        return Number(asteroid.attr('r')) > 30;
    }
    function breakDownAsteroid(asteroid) {
        if (canAsteroidBeBroken(asteroid) == true) {
            const newAsteroid1 = createAsteroid(new Elem(svg, 'circle'))(Number(asteroid.attr('cx')))(Number(asteroid.attr('cy')))(Number(asteroid.attr('r')) / 2)('gainsboro')('false')('white'), newAsteroid2 = createAsteroid(new Elem(svg, 'circle'))(Number(asteroid.attr('cx')))(Number(asteroid.attr('cy')))(Number(asteroid.attr('r')) / 2)('gainsboro')('false')('white');
            asteroidsList.push(newAsteroid1);
            asteroidsList.push(newAsteroid2);
            randomizeAsteroidMovement(newAsteroid1);
            randomizeAsteroidMovement(newAsteroid2);
            checkShipCollision(newAsteroid1);
            checkShipCollision(newAsteroid2);
        }
    }
    function randomizeAsteroidMovement(asteroid) {
        let asteroidMovement = Observable.interval(50).takeUntil(mainClock.filter(() => isShipHit == true || hasPlayerWon == true));
        let angleForX = generateRandom(360);
        let angleForY = generateRandom(360);
        asteroidMovement
            .map(() => ({ x: Number(asteroid.attr('cx')) + Math.sin(toRad(angleForX)),
            y: Number(asteroid.attr('cy')) - Math.cos(toRad(angleForY)),
            r: asteroid.attr('r') }))
            .subscribe(({ x, y }) => asteroid.attr('cx', x)
            .attr('cy', y));
        asteroidMovement
            .filter(() => (Number(asteroid.attr('cx')) > (600 + Number(asteroid.attr('r')))) && (Number(asteroid.attr('cx')) < (600 + Number(asteroid.attr('r')) + 5)))
            .subscribe(() => asteroid.attr('cx', 0));
        asteroidMovement
            .filter(() => Number(asteroid.attr('cx')) < 0)
            .subscribe(() => asteroid.attr('cx', (600 + Number(asteroid.attr('r')))));
        asteroidMovement
            .filter(() => (Number(asteroid.attr('cy')) > (600 + Number(asteroid.attr('r')))) && (Number(asteroid.attr('cy')) < (600 + Number(asteroid.attr('r')) + 5)))
            .subscribe(() => asteroid.attr('cy', 0));
        asteroidMovement
            .filter(() => Number(asteroid.attr('cy')) < 0)
            .subscribe(() => asteroid.attr('cy', (600 + Number(asteroid.attr('r')))));
    }
    function getDistance(point_x1, point_x2, point_y1, point_y2) {
        return Math.sqrt(Math.pow(point_x2 - point_x1, 2) + Math.pow(point_y2 - point_y1, 2));
    }
    function checkAsteroidList() {
        return asteroidsList.length == 0;
    }
    function displayButton() {
        const restartGameButton = new Elem(svg, 'rect').attr('x', 250).attr('y', 325).attr('width', 75).attr('height', 50).attr('fill', "#ffffff00").attr('stroke', 'yellow');
        restartGameButton.observe('mousedown').subscribe(() => location.reload());
        const restartText = new Elem(svg, 'text').attr('x', 260).attr('y', 350).attr('style', 'fill:white;stroke:white;font-size:15px').attr('id', 'restartText');
        const restart = document.getElementById('restartText');
        restart.innerHTML = "Restart";
    }
    function removeLife() {
        let remove = obs;
        remove
            .filter(() => playerLife == 2)
            .subscribe(() => life1.elem.remove());
        remove
            .filter(() => playerLife == 1)
            .subscribe(() => life2.elem.remove());
        remove
            .filter(() => playerLife == 0)
            .subscribe(() => life3.elem.remove());
    }
    function checkShipCollision(asteroid) {
        let collision = obs;
        collision
            .filter(() => getDistance(x, Number(asteroid.attr('cx')), y, Number(asteroid.attr('cy'))) < 15 + Number(asteroid.attr('r')))
            .map(() => (playerLife -= 1))
            .map(() => removeLife())
            .filter(() => playerLife == 0)
            .map(() => (isShipHit = true))
            .subscribe(() => { printLoseMessage(); });
        collision
            .filter(() => getDistance(x, Number(asteroid.attr('cx')), y, Number(asteroid.attr('cy'))) < 15 + Number(asteroid.attr('r')))
            .subscribe(() => { x = 300, y = 300; });
    }
    function printLoseMessage() {
        const playerLost = new Elem(svg, 'text').attr('x', 75).attr('y', 300).attr('style', 'fill:white;stroke:white;font-size:20px').attr('id', 'playerLost');
        const playerLostMsg = document.getElementById('playerLost');
        playerLostMsg.innerHTML = "Your ship got hit by an asteroid! The game is over!";
        const playerLost2 = new Elem(svg, 'text').attr('x', 100).attr('y', 320).attr('style', 'fill:white;stroke:white;font-size:20px').attr('id', 'playerLost2');
        const playerLostMsg2 = document.getElementById('playerLost2');
        playerLostMsg2.innerHTML = "Click the button below to restart the game!";
        displayButton();
    }
    function checkAsteroidBulletCollision(asteroid, bullet) {
        return getDistance(Number(bullet.attr('x')), Number(asteroid.attr('cx')), Number(bullet.attr('y')), Number(asteroid.attr('cy'))) < Number(asteroid.attr('r'));
    }
    function wrap() {
        wrapAround
            .filter(() => x > 620)
            .subscribe(() => x = 20);
        wrapAround
            .filter(() => x < 0)
            .subscribe(() => x = 620);
        wrapAround
            .filter(() => y < 0)
            .subscribe(() => y = 620);
        wrapAround
            .filter(() => y > 620)
            .subscribe(() => y = 20);
    }
    wrap();
    asteroidsList = createAsteroids(generateRandomAbove(10, 5));
    asteroidsList.forEach(element => randomizeAsteroidMovement(element));
    asteroidsList.forEach(element => checkShipCollision(element));
}
if (typeof window != 'undefined')
    window.onload = () => {
        asteroids();
    };
//# sourceMappingURL=asteroids.js.map