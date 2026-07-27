extends Area2D

@export var you_won_menu: NodePath
@onready var menu = get_node(you_won_menu)

func _ready():
	if menu:
		menu.visible = false  # Hide menu at start


func _on_body_entered(body: Area2D):
	print("here")
	if body.is_in_group("Player"):  # Make sure your player is in the "player" group!
		if menu:
			menu.visible = true
			get_tree().paused = true
