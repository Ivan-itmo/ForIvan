package moves;

import java.util.Random;

public class Sword implements Weapon{
    Random random = new Random();
    private int attack;
    @Override
    public int damage(){
        attack = random.nextInt(41);
        return attack;
    }
    @Override
    public String toString(){
        return "Sword";
    }
}
