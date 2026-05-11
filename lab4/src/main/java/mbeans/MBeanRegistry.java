package mbeans;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import java.lang.management.ManagementFactory;

public final class MBeanRegistry {
    private static final PointStats POINT_STATS = new PointStats();
    private static final Area AREA = new Area();

    private MBeanRegistry() {
    }

    static {
        try {
            MBeanServer server = ManagementFactory.getPlatformMBeanServer();
            if (!server.isRegistered(new ObjectName("lab4:type=PointStats"))) {
                server.registerMBean(POINT_STATS, new ObjectName("lab4:type=PointStats"));
            }
            if (!server.isRegistered(new ObjectName("lab4:type=Area"))) {
                server.registerMBean(AREA, new ObjectName("lab4:type=Area"));
            }
        } catch (Exception e) {
            throw new IllegalStateException("Не удалось зарегистрировать MBean", e);
        }
    }

    public static PointStats getPointStats() {
        return POINT_STATS;
    }

    public static Area getArea() {
        return AREA;
    }
}
