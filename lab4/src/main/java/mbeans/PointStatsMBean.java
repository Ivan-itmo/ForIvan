package mbeans;

public interface PointStatsMBean {
    int getTotalPoints();
    int getPointsInArea();
    int getConsecutiveMisses();
    void registerPoint(boolean hit);
}
