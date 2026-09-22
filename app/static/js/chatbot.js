const SMARTLEAD_API_URL = "https://smartlead-simatrix.onrender.com";

async function smartleadApiRequest(endpoint, options = {}) {
    const response = await fetch(`${SMARTLEAD_API_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.hata || "Sunucuyla iletişim kurulamadı.");
    }

    return data;
}

async function mesajGonder(mesaj, gecmis = []) {
    return smartleadApiRequest("/api/sohbet", {
        method: "POST",
        body: JSON.stringify({ mesaj, gecmis })
    });
}

async function leadKaydet(isim, telefon, eposta = "") {
    return smartleadApiRequest("/api/leads", {
        method: "POST",
        body: JSON.stringify({ isim, telefon, eposta })
    });
}

window.SmartleadChatbot = {
    mesajGonder,
    leadKaydet
};
