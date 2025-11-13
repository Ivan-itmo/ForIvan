// beans/LoginBean.java
package beans;

import entities.User;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.UserTransaction;
import java.io.Serializable;
import java.util.Date;

@Named("loginBean")
@SessionScoped
public class LoginBean implements Serializable {

    @PersistenceContext(unitName = "mainDB")
    private EntityManager em;

    @Inject
    private UserTransaction utx;

    private String username;
    private String password;

    private User currentUser;

    // === Вход (только для существующих пользователей) ===
    public String login() {
        try {
            TypedQuery<User> query = em.createQuery(
                    "SELECT u FROM User u WHERE u.username = :username", User.class);
            query.setParameter("username", username);
            User user = query.getSingleResult();

            if (!user.getPassword().equals(password)) {
                addErrorMessage("Неверный пароль");
                return null;
            }

            currentUser = user;
            return "main?faces-redirect=true";

        } catch (Exception e) {
            addErrorMessage("Пользователь не найден");
            return null;
        }
    }

    // === Регистрация (только для новых пользователей) ===
    public String register() {
        try {
            // Проверяем, не занят ли логин
            TypedQuery<Long> countQuery = em.createQuery(
                    "SELECT COUNT(u) FROM User u WHERE u.username = :username", Long.class);
            countQuery.setParameter("username", username);
            if (countQuery.getSingleResult() > 0) {
                addErrorMessage("Логин уже занят");
                return null;
            }

            // Создаём нового пользователя
            utx.begin();
            User newUser = new User();
            newUser.setUsername(username);
            newUser.setPassword(password); // ← для демо
            em.persist(newUser);
            utx.commit();

            currentUser = newUser;
            return "main?faces-redirect=true";

        } catch (Exception e) {
            rollbackIfNeeded();
            addErrorMessage("Ошибка регистрации: " + e.getMessage());
            return null;
        }
    }

    public String logout() {
        currentUser = null;
        // Инвалидация сессии (опционально, но рекомендуется)
        jakarta.faces.context.FacesContext.getCurrentInstance()
                .getExternalContext()
                .invalidateSession();
        return "start?faces-redirect=true";
    }

    // --- Вспомогательные методы ---
    private void addErrorMessage(String msg) {
        jakarta.faces.context.FacesContext.getCurrentInstance().addMessage(
                null,
                new jakarta.faces.application.FacesMessage(
                        jakarta.faces.application.FacesMessage.SEVERITY_ERROR, msg, null
                )
        );
    }

    private void rollbackIfNeeded() {
        try {
            if (utx != null && utx.getStatus() == jakarta.transaction.Status.STATUS_ACTIVE) {
                utx.rollback();
            }
        } catch (Exception ex) {
            // Игнор
        }
    }

    // Геттеры и сеттеры
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public User getCurrentUser() { return currentUser; }
}