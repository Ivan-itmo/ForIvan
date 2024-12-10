package characters;

import moves.*;

public class WildmanSpear extends Wildman {
    private final Spear spear;
    public WildmanSpear(String name, int height, int weight, Weapon weapon) {
        super(name, height, weight);
        this.spear = (Spear) weapon;
    }
    @Override
    public final void setDamage(MainCharacter character){
        character.takeDamage(spear.damage(), getName());

    }
    @Override
    public final void hello(){
        System.out.println("Появился солдат из племени " + getName() + " " + "рост " + getHeight() + " " + "вес " + getWeight() + " " + "оружие " + spear.toString());
    }

}