def get_breathing_tips():
    return {
        "breathing": "Let’s breathe some calm into your day: Inhale for 4 seconds, hold for 4, exhale for 4. Repeat 3 times—it’s like a mini reset!",
        "meditation": "How about a quick meditation? Get comfy, close your eyes if you’d like, and just follow your breath—in and out. A minute of this can work wonders.",
        "stress": "To shake off stress: Stretch your arms up, then lower them slowly as you exhale. Wiggle your fingers, then take 5 deep breaths. Feel lighter yet?",
        "affirmation": random_affirmation()
    }

def random_affirmation():
    import random
    affirmations = [
        "You’re a total rockstar, shining in your own way.",
        "You’ve got this—and I’ve got your back!",
        "Every little moment you shine is pure magic."
    ]
    return random.choice(affirmations)
