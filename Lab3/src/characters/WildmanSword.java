package characters;

import moves.*;

public class WildmanSword extends Wildman {
    private final Sword sword;
    public WildmanSword(String name, int height, int weight, Weapon weapon) {
        super(name, height, weight);
        this.sword = (Sword) weapon;
    }
    @Override
    public final void setDamage(MainCharacter character){
        character.takeDamage(sword.damage(), getName());
    }
    @Override
    public final void hello(){
        System.out.println("Появился солдат из племени " + getName() + " " + "рост " + getHeight() + " " + "вес " + getWeight() + " " + "оружие " + sword.toString());
    }

}
