package mbeans;

import javax.management.MBeanNotificationInfo;
import javax.management.Notification;
import javax.management.NotificationBroadcasterSupport;

public class PointStats extends NotificationBroadcasterSupport implements PointStatsMBean {
    private static final String THREE_MISSES_NOTIFICATION = "lab4.pointstats.threeConsecutiveMisses";

    private int totalPoints;
    private int pointsInArea;
    private int consecutiveMisses;
    private long notificationSequence = 1;

    @Override
    public synchronized int getTotalPoints() {
        return totalPoints;
    }

    @Override
    public synchronized int getPointsInArea() {
        return pointsInArea;
    }

    @Override
    public synchronized int getConsecutiveMisses() {
        return consecutiveMisses;
    }

    @Override
    public synchronized void registerPoint(boolean hit) {
        totalPoints++;
        if (hit) {
            pointsInArea++;
            consecutiveMisses = 0;
            return;
        }

        consecutiveMisses++;
        if (consecutiveMisses == 3) {
            sendThreeMissesNotification();
        }
    }

    @Override
    public MBeanNotificationInfo[] getNotificationInfo() {
        String[] notificationTypes = {THREE_MISSES_NOTIFICATION};
        String notificationClassName = Notification.class.getName();
        String description = "Уведомление о трех промахах подряд";
        return new MBeanNotificationInfo[] {
                new MBeanNotificationInfo(notificationTypes, notificationClassName, description)
        };
    }

    private void sendThreeMissesNotification() {
        sendNotification(new Notification(
                THREE_MISSES_NOTIFICATION,
                this,
                notificationSequence++,
                "Пользователь совершил 3 промаха подряд"
        ));
    }
}
