extends Node

var has_started := false
var game_over := false

func _ready():
	print("GlobalManager ready. has_started:", has_started, " game_over:", game_over)
