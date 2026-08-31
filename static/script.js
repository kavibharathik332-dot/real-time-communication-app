/* ============================================================
   Real-Time Communication App - Client-side logic
   ============================================================
   This file:
     - connects to the Flask-SocketIO server
     - loads the list of registered users
     - loads chat history when a user is selected
     - sends and receives messages instantly
     - shows online/offline status
     - shows the typing indicator
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {
  const appEl = document.getElementById("chat-app");
  const myUserId = parseInt(appEl.dataset.userId, 10);

  // ---- DOM elements ----
  const userListEl = document.getElementById("user-list");
  const searchInput = document.getElementById("search-users");
  const chatPlaceholder = document.getElementById("chat-placeholder");
  const chatWindow = document.getElementById("chat-window");
  const chatHeaderName = document.getElementById("chat-header-name");
  const chatHeaderStatus = document.getElementById("chat-header-status");
  const chatMessages = document.getElementById("chat-messages");
  const typingIndicator = document.getElementById("typing-indicator");
  const chatForm = document.getElementById("chat-input-form");
  const messageInput = document.getElementById("message-input");
  const chatError = document.getElementById("chat-error");

  // ---- App state ----
  let users = [];               // full list of other users: [{id, username}]
  let onlineUserIds = new Set(); // which user ids are currently online
  let selectedUser = null;      // the user currently being chatted with
  let typingTimeout = null;     // used to auto-clear "typing..." locally

  // ---- Connect to the Socket.IO server ----
  const socket = io();

  socket.on("connect", () => {
    socket.emit("get_online_users");
  });

  // ==========================================================
  // Loading and rendering the user list
  // ==========================================================

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function initials(name) {
    return name.trim().slice(0, 2).toUpperCase();
  }

  function loadUsers() {
    fetch("/api/users")
      .then((res) => res.json())
      .then((data) => {
        users = data;
        renderUserList();
      })
      .catch(() => {
        userListEl.innerHTML = '<li class="user-list-empty">Could not load users.</li>';
      });
  }

  function renderUserList() {
    const filter = searchInput.value.trim().toLowerCase();
    const filtered = users.filter((u) => u.username.toLowerCase().includes(filter));

    if (filtered.length === 0) {
      userListEl.innerHTML = '<li class="user-list-empty">No users found.</li>';
      return;
    }

    userListEl.innerHTML = "";
    filtered.forEach((u) => {
      const isOnline = onlineUserIds.has(u.id);
      const li = document.createElement("li");
      li.className = "user-item" + (selectedUser && selectedUser.id === u.id ? " active" : "");
      li.dataset.userId = u.id;
      li.innerHTML = `
        <div class="avatar">${escapeHtml(initials(u.username))}</div>
        <div class="user-info">
          <span class="username">${escapeHtml(u.username)}</span>
          <span class="status-text">
            <span class="status-dot ${isOnline ? "online" : ""}"></span>
            ${isOnline ? "Online" : "Offline"}
          </span>
        </div>
      `;
      li.addEventListener("click", () => selectUser(u));
      userListEl.appendChild(li);
    });
  }

  searchInput.addEventListener("input", renderUserList);

  // ==========================================================
  // Selecting a user to chat with
  // ==========================================================

  function selectUser(user) {
    selectedUser = user;
    chatPlaceholder.classList.add("hidden");
    chatWindow.classList.remove("hidden");
    chatHeaderName.textContent = user.username;
    updateHeaderStatus();
    typingIndicator.classList.add("hidden");
    chatError.classList.add("hidden");
    renderUserList();
    loadHistory(user.id);
    messageInput.focus();
  }

  function updateHeaderStatus() {
    if (!selectedUser) return;
    const isOnline = onlineUserIds.has(selectedUser.id);
    chatHeaderStatus.textContent = isOnline ? "Online" : "Offline";
  }

  function loadHistory(otherUserId) {
    chatMessages.innerHTML = '<p style="text-align:center;color:#9ca3af;font-size:13px;">Loading messages...</p>';
    fetch(`/api/messages/${otherUserId}`)
      .then((res) => res.json())
      .then((messages) => {
        chatMessages.innerHTML = "";
        if (messages.length === 0) {
          chatMessages.innerHTML = '<p style="text-align:center;color:#9ca3af;font-size:13px;">No messages yet. Say hello!</p>';
          return;
        }
        messages.forEach(appendMessage);
        scrollToBottom();
      });
  }

  function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function appendMessage(msg) {
    const isMine = msg.sender_id === myUserId;
    const bubble = document.createElement("div");
    bubble.className = "message-bubble " + (isMine ? "mine" : "theirs");
    // Using textContent (not innerHTML) for the message text prevents
    // the browser from running any HTML/JavaScript hidden in a message.
    const textNode = document.createElement("span");
    textNode.textContent = msg.message;
    const timeNode = document.createElement("span");
    timeNode.className = "msg-time";
    timeNode.textContent = formatTime(msg.created_at);
    bubble.appendChild(textNode);
    bubble.appendChild(timeNode);
    chatMessages.appendChild(bubble);
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // ==========================================================
  // Sending messages
  // ==========================================================

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!selectedUser) return;

    const text = messageInput.value.trim();
    if (!text) {
      showError("Message cannot be empty.");
      return;
    }

    socket.emit("send_message", { receiver_id: selectedUser.id, message: text });
    socket.emit("typing", { receiver_id: selectedUser.id, is_typing: false });
    messageInput.value = "";
  });

  function showError(text) {
    chatError.textContent = text;
    chatError.classList.remove("hidden");
    setTimeout(() => chatError.classList.add("hidden"), 3000);
  }

  socket.on("message_error", (data) => {
    showError(data.error || "Something went wrong.");
  });

  // ==========================================================
  // Receiving messages in real time
  // ==========================================================

  socket.on("new_message", (msg) => {
    const relevantUserId = msg.sender_id === myUserId ? msg.receiver_id : msg.sender_id;

    if (selectedUser && selectedUser.id === relevantUserId) {
      // Remove the "no messages yet" placeholder if present.
      if (chatMessages.children.length === 1 && chatMessages.textContent.includes("No messages yet")) {
        chatMessages.innerHTML = "";
      }
      appendMessage(msg);
      scrollToBottom();
    }
  });

  // ==========================================================
  // Typing indicator
  // ==========================================================

  messageInput.addEventListener("input", () => {
    if (!selectedUser) return;
    socket.emit("typing", { receiver_id: selectedUser.id, is_typing: true });

    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
      socket.emit("typing", { receiver_id: selectedUser.id, is_typing: false });
    }, 1500);
  });

  socket.on("typing_update", (data) => {
    if (selectedUser && selectedUser.id === data.sender_id) {
      if (data.is_typing) {
        typingIndicator.textContent = `${data.username} is typing...`;
        typingIndicator.classList.remove("hidden");
      } else {
        typingIndicator.classList.add("hidden");
      }
    }
  });

  // ==========================================================
  // Online / offline status
  // ==========================================================

  socket.on("online_users_list", (data) => {
    onlineUserIds = new Set(data.online_user_ids);
    renderUserList();
    updateHeaderStatus();
  });

  socket.on("status_update", (data) => {
    if (data.online) {
      onlineUserIds.add(data.user_id);
    } else {
      onlineUserIds.delete(data.user_id);
    }
    renderUserList();
    updateHeaderStatus();
  });

  // ---- Kick things off ----
  loadUsers();
});
