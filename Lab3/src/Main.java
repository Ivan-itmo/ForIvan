import exceptions.*;
import moves.*;
import characters.*;
import household.*;
import godness.*;

import java.util.InputMismatchException;
import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        try {
            System.out.println("Введите имя главного героя");
            String name = scanner.nextLine();

            System.out.println("Введите высоту главного героя в int");
            int height = scanner.nextInt();
            if (height < 0) {
                throw new NegativeNumberException();
            }

            System.out.println("Введите вес главного героя в int");
            int weight = scanner.nextInt();
            if (weight < 0) {
                throw new NegativeNumberException();
            }

            System.out.println("Введите здоровье главного героя в int");
            int health = scanner.nextInt();
            if (health < 0) {
                throw new NegativeNumberException();
            }

            System.out.println("Введите производительность главного героя в int");
            int performance = scanner.nextInt();
            if (performance < 0) {
                throw new NegativeNumberException();
            }

            System.out.println("Введите потребление главного героя в int");
            int intake = scanner.nextInt();
            if (intake < 0) {
                throw new NegativeNumberException();
            }

            int year = 485;
            God god = new God("Аллах", random.nextInt(3) + 1);
            god.hello();

            MainCharacter character = new MainCharacter(name, height, weight, health, performance, intake);
            character.hello();
            CharacterItems items = new CharacterItems(Item.values());
            Field field = new Field(random.nextInt(20) + 20);
            field.hello();

            Weapon weapon1 = new Sword();
            Weapon weapon2 = new Spear();
            Weapon weapon3 = new Axe();

            while (character.getLive()) {
                System.out.println("В " + year + " году произошло:");
                if (random.nextInt(2) == 0){
                    System.out.println("Дикие люди не пришли");
                    items.printItems(character);
                    character.starvation(field, god);
                }
                else {
                    System.out.println("Дикие люди пришли");

                    WildmanSword wildman1 = new WildmanSword("Enumai", random.nextInt(10) + 170, random.nextInt(10) + 70, weapon1);
                    wildman1.hello();
                    WildmanSpear wildman2 = new WildmanSpear("Kriks", random.nextInt(20) + 160, random.nextInt(20) + 65, weapon2);
                    wildman2.hello();
                    WildmanAxe wildman3 = new WildmanAxe("Barka", random.nextInt(15) + 190, random.nextInt(15) + 60, weapon3);
                    wildman3.hello();
                    Stoleman stoleman = new Stoleman("Ashyr", random.nextInt(5) + 150, random.nextInt(5) + 90, random.nextInt(130));
                    stoleman.hello();

                    wildman1.setDamage(character);
                    wildman2.setDamage(character);
                    wildman3.setDamage(character);

                    stoleman.processStole(character, items);
                    items.printItems(character);
                }
                year += 1;
                System.out.println();
            }
        } catch (InputMismatchException e) {
            System.out.println("int должен быть!");
        } catch (NegativeNumberException e) {
            System.out.println(e.getMessage());
        }


    }
}