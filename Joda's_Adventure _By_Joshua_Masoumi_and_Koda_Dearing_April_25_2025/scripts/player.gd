extends CharacterBody2D

const SPEED = 120.0
const JUMP_VELOCITY = -300.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

@export var win_position: Vector2  # Set this in the editor to your goal location
@export var win_menu: NodePath  # Drag your UI node (e.g., "YouWonMenu") into this in the editor

var has_won = false  # To avoid showing the menu multiple times


@onready var animated_sprite = $AnimatedSprite2D

var health = 3  # Basic health system

func _physics_process(delta):
	if not is_on_floor():
		velocity.y += gravity * delta

	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = JUMP_VELOCITY
		$JumpSound.play()

	var direction = Input.get_axis("move_left", "move_right")

	if direction > 0:
		animated_sprite.flip_h = false
	elif direction < 0:
		animated_sprite.flip_h = true

	if is_on_floor():
		if direction == 0:
			animated_sprite.play("idlesteve")
		else:
			animated_sprite.play("runsteve")
	else:
		animated_sprite.play("jumpsteve")

	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)

	move_and_slide()

	if not has_won and position.distance_to(win_position) < 10:
		show_win_menu()

func show_win_menu():
	has_won = true
	var win_node = get_node(win_menu)
	win_node.visible = true
	get_tree().paused = true

func take_damage(amount):
	health -= amount
	if health <= 0:
		die()
func die():
	if get_tree().paused:
		return
	$CanvasLayer/GameOverMenu.show_menu()
	
