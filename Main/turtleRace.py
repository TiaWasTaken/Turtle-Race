import turtle
import time
import random
import json
import os

WIDTH, HEIGHT = 500, 500
COLORS = ["red", "blue", "green", "black", "purple", "yellow", "cyan"]

COLOR_MAP = {
    "red": "\033[1;31;40mred\033[0m",
    "blue": "\033[1;34;40mblue\033[0m",
    "green": "\033[1;32;40mgreen\033[0m",
    "black": "\033[1;30;40mblack\033[0m",
    "purple": "\033[1;35;40mpurple\033[0m",
    "yellow": "\033[1;33;40myellow\033[0m",
    "cyan": "\033[1;36;40mcyan\033[0m",
}

EMOJIS = ["😐", "👽", "🤖", "👾", "🐶", "🐱", "🦊", "🐸", "🐼", "🐨", "🐷"]

BALANCES_FILE = "balances.json"


def load_balances():
    if not os.path.exists(BALANCES_FILE):
        return {}
    with open(BALANCES_FILE, "r") as file:
        return json.load(file)


def save_balances(balances):
    with open(BALANCES_FILE, "w") as file:
        json.dump(balances, file, indent=4)


def get_balance(balances):
    while True:
        choice = input(
            "\n\033[1;34;40mDo you want to (Enter 1 or 2): \n(1) add a new balance or \n(2) choose an existing balance?\033[0m\n\n"
        )
        if choice == "1":
            name = input("\n\033[1;33;40mEnter a name for the new balance:\033[0m ")
            if name in balances:
                print(
                    "\n\033[1;31;40mA balance with this name already exists. Please choose another name.\033[0m"
                )
            else:
                print("\n\033[1;32;40mSelect an emoji for your account:\033[0m\n")
                for i, emoji in enumerate(EMOJIS):
                    print(f"{i + 1}: {emoji}")
                while True:
                    emoji_choice = input(
                        "\n\033[1;36;40mEnter the number corresponding to your chosen emoji:\033[0m "
                    )
                    if emoji_choice.isdigit() and 1 <= int(emoji_choice) <= len(EMOJIS):
                        emoji = EMOJIS[int(emoji_choice) - 1]
                        break
                    else:
                        print("\n\033[1;31;40mInvalid choice. Please try again.\033[0m")
                balances[name] = {"balance": 100, "emoji": emoji}
                save_balances(balances)
                return name, balances[name]
        elif choice == "2":
            if not balances:
                print(
                    "\n\033[1;31;40mNo existing balances found. Please add a new balance.\033[0m"
                )
            else:
                print("\n\033[1;32;40mExisting balances:\033[0m\n")
                for name, info in balances.items():
                    print(f"{name} {info['emoji']}")
                name = input(
                    "\n\033[1;36;40mEnter the name of the balance to use:\033[0m "
                )
                if name in balances:
                    return name, balances[name]
                else:
                    print(
                        "\n\033[1;31;40mNo balance found with this name. Please try again.\033[0m"
                    )
        else:
            print("\n\033[1;31;40mInvalid choice. Please enter 1 or 2.\033[0m\n")


def get_number_of_racers():
    while True:
        racers = input("\n🏁 \033[1;32;40mEnter the number of racers (2 - 7):\033[0m ")
        if racers.isdigit():
            racers = int(racers)
            if 2 <= racers <= 7:
                return racers
            else:
                print(
                    "\n\033[1;31;40mNumber not in range 2-7. Please try again.\033[0m"
                )
        else:
            print("\n\033[1;31;40mInput is not numeric... Please try again.\033[0m")


def get_bet(colors, balance):
    while True:
        print("\n✅ \033[1;32;40mAvailable turtles for the race:\033[0m\n")
        for color in colors:
            print(COLOR_MAP[color])

        selected_color = input(
            "\n\033[1;33;40mSelect a turtle color to bet on:\033[0m "
        )
        if selected_color not in colors:
            print(
                "\n\033[1;31;40mSelected color is not in the race. Please try again.\033[0m"
            )
            continue

        while True:
            bet_amount = input(
                "\n\033[1;33;40mEnter the amount of money to bet:\033[0m "
            )
            if bet_amount.isdigit():
                bet_amount = int(bet_amount)
                if bet_amount <= balance:
                    return selected_color, bet_amount
                else:
                    print(
                        "\n\033[1;31;40mYou don't have enough balance. Please try again.\033[0m\n"
                    )
            else:
                print(
                    "\n\033[1;31;40mBet amount is not numeric... Please try again.\033[0m\n"
                )


def race(colors):
    turtles = create_turtle(colors)  # Create turtles

    while True:
        for racer in turtles:
            distance = random.randrange(1, 5)
            racer.forward(distance)

            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[
                    turtles.index(racer)
                ]  # Return the color of the winning turtle


def create_turtle(colors):
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape("turtle")
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDTH // 2 + (i + 1) * spacingx, -HEIGHT // 2 + 20)
        racer.pendown()
        turtles.append(racer)
    return turtles


def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing Game")
    return screen


def main():
    balances = load_balances()
    name, info = get_balance(balances)
    balance = info["balance"]
    emoji = info["emoji"]

    if balance == 0:
        print("\n\033[1;31;40mYour balance is 0. Re-loading with $100.\033[0m\n")
        balance = 100

    racers = get_number_of_racers()
    random.shuffle(COLORS)
    colors = COLORS[:racers]

    print(
        f"\n{emoji} \033[1;32;40m{name}, your current balance is: ${balance}\033[0m\n"
    )
    selected_color, bet_amount = get_bet(colors, balance)

    screen = init_turtle()

    winner = race(colors)
    print(
        f"\n🏆 \033[1;32;40mThe winner is the turtle with color: {COLOR_MAP[winner]}\033[0m\n"
    )

    if winner == selected_color:
        balance += bet_amount * (racers + 1)
        print(
            f"🎉 \033[1;32;40mCongratulations! You won ${bet_amount * (racers + 1)}\033[0m\n"
        )
    else:
        balance -= bet_amount
        print(f"👎 \033[1;31;40mSorry, you lost ${bet_amount}\033[0m")

    print(f"\n💵 \033[1;32;40mYour final balance is: ${balance}\033[0m\n")
    balances[name]["balance"] = balance
    save_balances(balances)

    print("\033[1;33;40mClosing window in 2 seconds...\033[0m")
    time.sleep(2)
    screen.bye()


if __name__ == "__main__":
    main()
