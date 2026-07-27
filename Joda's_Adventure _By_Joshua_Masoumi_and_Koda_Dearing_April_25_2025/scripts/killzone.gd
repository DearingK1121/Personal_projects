extends Area2D

@export var game_over_menu: NodePath  # Drag in your menu in the editor
@onready var timer = $Timer

#func _ready():
	#if has_node(game_over_menu):
		#get_node(game_over_menu).visible = false

func _on_body_entered(body):
	if body.name == "Player":
		print("You died!")
		Engine.time_scale = 0.5
		body.get_node("CollisionShape2D").queue_free()
		timer.start()
	

func _on_timer_timeout():
	Engine.time_scale = 1.0
	#if has_node(game_over_menu):
		#get_node(game_over_menu).visible = true
		#get_tree().paused = true
	get_tree().reload_current_scene()
