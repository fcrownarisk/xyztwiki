import * as THREE from 'three';

class FirstPersonController {
    constructor(camera) {
        this.camera = camera;
        this.position = new THREE.Vector3(0, 0, 0);
        this.velocity = new THREE.Vector3();
        this.rotation = new THREE.Euler(0, 0, 0, 'XYZ');
        
        // Movement settings
        this.speed = 5;
        this.sprintMultiplier = 2;
        this.jumpForce = 4;
        this.gravity = 9.8;
        this.isGrounded = true;

        // Mouse control
        this.mouse = new THREE.Vector2();
        this.prevMouse = new THREE.Vector2();
        this.lookSpeed = 0.002;

        // Key states
        this.keys = {
            w: false,
            a: false,
            s: false,
            d: false,
            space: false,
            shift: false
        };

        // Setup event listeners
        this.setupControls();
    }

    setupControls() {
        // Keyboard events
        document.addEventListener('keydown', (e) => this.onKeyDown(e));
        document.addEventListener('keyup', (e) => this.onKeyUp(e));

        // Mouse events
        document.addEventListener('mousemove', (e) => this.onMouseMove(e));
        document.addEventListener('click', () => {
            document.body.requestPointerLock();
        });
    }

    onKeyDown(e) {
        switch(e.code) {
            case 'KeyW': this.keys.w = true; break;
            case 'KeyA': this.keys.a = true; break;
            case 'KeyS': this.keys.s = true; break;
            case 'KeyD': this.keys.d = true; break;
            case 'Space': this.keys.space = true; break;
            case 'ShiftLeft': this.keys.shift = true; break;
        }
    }

    onKeyUp(e) {
        switch(e.code) {
            case 'KeyW': this.keys.w = false; break;
            case 'KeyA': this.keys.a = false; break;
            case 'KeyS': this.keys.s = false; break;
            case 'KeyD': this.keys.d = false; break;
            case 'Space': this.keys.space = false; break;
            case 'ShiftLeft': this.keys.shift = false; break;
        }
    }

    onMouseMove(e) {
        if (document.pointerLockElement === document.body) {
            this.mouse.x = e.movementX;
            this.mouse.y = e.movementY;
        }
    }

    update(delta) {
        // Calculate movement speed
        const currentSpeed = this.keys.shift ? 
            this.speed * this.sprintMultiplier : 
            this.speed;

        // Apply gravity
        if (!this.isGrounded) {
            this.velocity.y -= this.gravity * delta;
        }

        // Jumping
        if (this.keys.space && this.isGrounded) {
            this.velocity.y = this.jumpForce;
            this.isGrounded = false;
        }

        // Calculate movement direction
        const direction = new THREE.Vector3();
        const rotation = this.rotation.y;

        if (this.keys.w) direction.z -= 1;
        if (this.keys.s) direction.z += 1;
        if (this.keys.a) direction.x -= 1;
        if (this.keys.d) direction.x += 1;

        direction.normalize();
        direction.applyAxisAngle(new THREE.Vector3(0, 1, 0), rotation);

        // Update velocity
        this.velocity.x = direction.x * currentSpeed;
        this.velocity.z = direction.z * currentSpeed;

        // Update position
        this.position.addScaledVector(this.velocity, delta);

        // Update camera rotation
        this.rotation.y -= this.mouse.x * this.lookSpeed;
        this.rotation.x -= this.mouse.y * this.lookSpeed;
        this.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, this.rotation.x));

        // Update camera position and rotation
        this.camera.position.copy(this.position);
        this.camera.rotation.set(this.rotation.x, this.rotation.y, 0);

        // Reset mouse movement
        this.mouse.set(0, 0);
    }
}

// Usage example:
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create player controller
const controller = new FirstPersonController(camera);

// Simple floor
const floorGeometry = new THREE.PlaneGeometry(10, 10);
const floorMaterial = new THREE.MeshBasicMaterial({color: 0x444444, side: THREE.DoubleSide});
const floor = new THREE.Mesh(floorGeometry, floorMaterial);
floor.rotation.x = Math.PI/2;
scene.add(floor);

// Animation loop
let clock = new THREE.Clock();
function animate() {
    const delta = clock.getDelta();
    
    // Update controller
    controller.update(delta);

    // Simple ground check
    controller.isGrounded = controller.position.y <= 0;
    if (controller.position.y < 0) {
        controller.position.y = 0;
        controller.velocity.y = 0;
    }

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

animate();
