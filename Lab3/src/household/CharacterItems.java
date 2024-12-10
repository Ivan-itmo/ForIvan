package household;
import characters.MainCharacter;


public class CharacterItems {
    private Item[] items;
    public CharacterItems(Item[] items) {
        this.items = items;
    }
    public final void printItems(MainCharacter character){
        if (character.getLive() && items.length > 0) {
            System.out.println("Главный персонаж " + character.getName() + " имеет собственность:");
            for (Item p : items) {
                System.out.println(p.toString());
            }
        }
    }
    /*
    public int getLength(Item[] items){
        int c = 0;
        for (Item p : items) {
            c += 1;
        }
        return c;
    }
    */
    public final Item[] getProperty(){
        return items;
    }
    public final void setProperty(Item[] items){
        this.items = items;
    }
}
