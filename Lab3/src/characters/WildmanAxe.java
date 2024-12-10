package characters;

import moves.*;

public class WildmanAxe extends Wildman {
    private final Axe axe;
    public WildmanAxe(String name, int height, int weight, Weapon weapon) {
        super(name, height, weight);
        this.axe = (Axe) weapon;
    }
    @Override
    public final void setDamage(MainCharacter character){
        character.takeDamage(axe.damage(), getName());

    }
    @Override
    public final void hello(){
        System.out.println("Появился солдат из племени " + getName() + " " + "рост " + getHeight() + " " + "вес " + getWeight() + " " + "оружие " + axe.toString());
    }

}