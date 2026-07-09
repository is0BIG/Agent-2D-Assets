extends CharacterBody2D

@export var speed: float = 140.0

@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D


func _physics_process(_delta: float) -> void:
	var direction := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	velocity = direction * speed
	move_and_slide()

	if direction.length() > 0.0:
		animated_sprite.play("walk")
	else:
		animated_sprite.play("idle")
