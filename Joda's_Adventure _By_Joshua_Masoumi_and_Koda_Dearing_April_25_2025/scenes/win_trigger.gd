extends Area2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_body_entered(body: Node2D) -> void:
	print("Something entered the trigger:", body.name)
	if body.is_in_group("Player"):  # Or use the node name if you prefer
		$victory.play()
		var menu = get_parent().get_node("YouWonMenu")  # Adjust path if needed!
		menu.visible = true
		get_tree().paused = false
