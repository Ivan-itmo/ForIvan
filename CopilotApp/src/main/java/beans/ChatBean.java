package beans;

import entities.*;
import javax.enterprise.context.SessionScoped;
import javax.inject.Inject;
import javax.inject.Named;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;
import javax.transaction.UserTransaction;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Named
@SessionScoped
public class ChatBean implements Serializable {

    @PersistenceContext(unitName = "mainDB")
    private EntityManager em;

    @Inject
    private UserTransaction utx;

    @Inject
    private LoginBean loginBean;

    private Chat currentChat;
    private String userInput;
    private String newChatTitle = "Новый чат"; // ← новое поле

    public void createNewChat() {
        if (newChatTitle == null || newChatTitle.trim().isEmpty()) {
            newChatTitle = "Новый чат";
        }
        try {
            utx.begin();
            Chat chat = new Chat();
            chat.setTitle(newChatTitle.trim());
            chat.setUser(loginBean.getCurrentUser());
            em.persist(chat);
            utx.commit();
            currentChat = chat;
            newChatTitle = "Новый чат";
        } catch (Exception e) {
            rollback();
        }
    }

    public void sendMessage() {
        if (userInput == null || userInput.trim().isEmpty()) return;

        try {
            if (currentChat == null) {
                createNewChat();
                if (currentChat == null) {
                    throw new RuntimeException("Не удалось создать чат");
                }
            }

            utx.begin();
            saveMessageWithoutTx("user", userInput);
            saveMessageWithoutTx("assistant", "Ответ от CopilotApp");
            utx.commit();

            userInput = "";
        } catch (Exception e) {
            rollback();
            throw new RuntimeException("Ошибка чата", e);
        }
    }

    private void saveMessageWithoutTx(String role, String content) {
        Message msg = new Message();
        msg.setContent(content);
        msg.setRole(role);
        msg.setChat(currentChat);
        em.persist(msg);
    }

    public List<Message> getMessages() {
        if (currentChat == null || currentChat.getId() == null) return new ArrayList<>();
        TypedQuery<Message> query = em.createQuery(
                "SELECT m FROM Message m WHERE m.chat = :chat ORDER BY m.id ASC",
                Message.class
        );
        query.setParameter("chat", currentChat);
        return query.getResultList();
    }

    public List<Chat> getUserChats() {
        if (loginBean.getCurrentUser() == null) {
            return new ArrayList<>();
        }
        TypedQuery<Chat> query = em.createQuery(
                "SELECT c FROM Chat c WHERE c.user = :user ORDER BY c.id DESC",
                Chat.class
        );
        query.setParameter("user", loginBean.getCurrentUser());
        return query.getResultList();
    }

    public void switchToChat(Chat chat) {
        this.currentChat = chat;
    }

    private void rollback() {
        try {
            if (utx != null && utx.getStatus() == javax.transaction.Status.STATUS_ACTIVE) {
                utx.rollback();
            }
        } catch (Exception ex) {
            // Игнорируем ошибку отката
        }
    }

    // Геттеры и сеттеры
    public String getUserInput() { return userInput; }
    public void setUserInput(String userInput) { this.userInput = userInput; }

    public Chat getCurrentChat() { return currentChat; }

    public String getNewChatTitle() { return newChatTitle; }
    public void setNewChatTitle(String newChatTitle) { this.newChatTitle = newChatTitle; }
}