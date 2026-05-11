package demo;

import entities.ResultEntry;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class DemoResultsStore {
    private final List<ResultEntry> results = new ArrayList<>();
    private final boolean optimized;
    private int hitCount;
    private String lastSummary = "";

    public DemoResultsStore(boolean optimized) {
        this.optimized = optimized;
    }

    public void add(ResultEntry entry) {
        results.add(entry);

        if (optimized) {
            updateFast(entry);
        } else {
            updateSlow();
        }
    }

    public int getResultsCount() {
        return results.size();
    }

    public int getHitCount() {
        return hitCount;
    }

    public String getLastSummary() {
        return lastSummary;
    }

    private void updateFast(ResultEntry entry) {
        if (Boolean.TRUE.equals(entry.getHit())) {
            hitCount++;
        }

        lastSummary = "results=" + results.size()
                + ", hits=" + hitCount
                + ", last=(" + entry.getX() + "," + entry.getY() + "," + entry.getR() + ")";
    }

    private void updateSlow() {
        List<ResultEntry> copy = new ArrayList<>(results);
        copy.sort(Comparator.comparing(ResultEntry::getTimestamp).reversed());

        int hits = 0;
        StringBuilder builder = new StringBuilder();
        for (ResultEntry result : copy) {
            if (Boolean.TRUE.equals(result.getHit())) {
                hits++;
            }

            builder.append(result.getX())
                    .append(':')
                    .append(result.getY())
                    .append(':')
                    .append(result.getR())
                    .append(':')
                    .append(result.getHit())
                    .append('|');
        }

        hitCount = hits;
        lastSummary = builder.toString();
    }
}
