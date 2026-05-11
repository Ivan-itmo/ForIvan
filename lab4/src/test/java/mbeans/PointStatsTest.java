package mbeans;

import org.junit.jupiter.api.Test;

import javax.management.Notification;
import javax.management.NotificationListener;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PointStatsTest {

    @Test
    void shouldCountTotalPointsPointsInAreaAndConsecutiveMisses() {
        PointStats stats = new PointStats();

        stats.registerPoint(true);
        stats.registerPoint(false);
        stats.registerPoint(false);

        assertEquals(3, stats.getTotalPoints());
        assertEquals(1, stats.getPointsInArea());
        assertEquals(2, stats.getConsecutiveMisses());
    }

    @Test
    void shouldSendNotificationAfterThreeConsecutiveMisses() {
        PointStats stats = new PointStats();
        List<Notification> notifications = new ArrayList<>();
        NotificationListener listener = (notification, handback) -> notifications.add(notification);
        stats.addNotificationListener(listener, null, null);

        stats.registerPoint(false);
        stats.registerPoint(false);
        stats.registerPoint(false);

        assertEquals(1, notifications.size());
        assertEquals("lab4.pointstats.threeConsecutiveMisses", notifications.get(0).getType());
        assertEquals(3, stats.getConsecutiveMisses());
    }
}
