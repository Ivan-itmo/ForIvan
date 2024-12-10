package godness;

public record God (String name, int buffFertility) {
    public void hello(){
        System.out.println("Появился бог " + name + " который может увеличить плодородность в " + buffFertility + " раза");
    }
}
