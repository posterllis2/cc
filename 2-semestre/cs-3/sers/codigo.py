import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import time
from datetime import datetime

# CONFIGURAÇÕES DA ESTAÇÃO E CORES
POTENCIA_NOMINAL_VAGA = 7.0  
LIMITE_POTENCIA_HUB = 15.0  
TARIFA_BASE_COMERCIAL = 0.80 

# Paleta de Cores 
BG_COLOR = "#0D0D0D"        # Preto Fundo
PANEL_COLOR = "#1A1A1A"     # Preto Painéis
ACCENT_COLOR = "#E63946"    # Vermelho Principal
ACCENT_HOVER = "#D62828"    # Vermelho Escuro (Hover)
TEXT_COLOR = "#FFFFFF"      # Branco
TEXT_MUTED = "#A8DADC"      # Azul claro/Cinza para textos secundários
SUCCESS_COLOR = "#2A9D8F"   # Verde para sucesso/solar

class ReechargeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("REECHARGE - Central de Controle Inteligente")
        self.root.geometry("1000x700")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 600)

        # Variáveis de Estado
        self.vagas = {}
        self.historico_geral = []
        self.hora_simulada = 12
        self.geracao_solar = 0.0

        self.setup_ui()
        self.atualizar_estado_sistema()
        self.log_mensagem("SISTEMA INICIADO: Estação REECHARGE online.", ACCENT_COLOR)
        self.simular_log_ocpp("BootNotification", {"chargePointModel": "GW-7KW-EV", "chargePointVendor": "GoodWe"})

    def setup_ui(self):
        # HEADER
        header_frame = tk.Frame(self.root, bg=ACCENT_COLOR, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_label = tk.Label(header_frame, text="⚡ REECHARGE - GESTÃO COMERCIAL DE VEs", 
                                bg=ACCENT_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 16, "bold"))
        header_label.pack(pady=15)

        # CONTAINER PRINCIPAL 
        main_container = tk.Frame(self.root, bg=BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # SIDEBAR (Botões)
        sidebar = tk.Frame(main_container, bg=PANEL_COLOR, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))

        lbl_menu = tk.Label(sidebar, text="PAINEL DE CONTROLE", bg=PANEL_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 12, "bold"))
        lbl_menu.pack(pady=20)

        botoes = [
            ("🔌 Conectar Veículo", self.popup_conectar_veiculo),
            ("⚡ Simular Carga (+)", self.simular_ciclo_recarga),
            ("💳 Liberar & Pagar", self.popup_pagamento),
            ("🤖 Acionar IA", self.acionar_ia),
            ("⏰ Avançar Tempo", self.avancar_tempo),
            ("💾 Exportar e Sair", self.exportar_sair)
        ]

        for texto, comando in botoes:
            btn = tk.Button(sidebar, text=texto, bg=ACCENT_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, command=comando, cursor="hand2", pady=10)
            btn.pack(fill=tk.X, padx=20, pady=8)

        # ÁREA CENTRAL (Dashboards e Vagas)
        center_frame = tk.Frame(main_container, bg=BG_COLOR)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Dashboard Topo
        dash_frame = tk.Frame(center_frame, bg=PANEL_COLOR)
        dash_frame.pack(fill=tk.X, pady=(0, 20))

        self.lbl_hora = tk.Label(dash_frame, text="🕒 Hora: 12:00", bg=PANEL_COLOR, fg=TEXT_COLOR, font=("Consolas", 14))
        self.lbl_hora.pack(side=tk.LEFT, padx=20, pady=15)

        self.lbl_solar = tk.Label(dash_frame, text="☀️ Solar: 0.0 kW", bg=PANEL_COLOR, fg=SUCCESS_COLOR, font=("Consolas", 14, "bold"))
        self.lbl_solar.pack(side=tk.LEFT, padx=20, pady=15)

        self.lbl_potencia = tk.Label(dash_frame, text="⚡ Disp: 15.0 kW", bg=PANEL_COLOR, fg=TEXT_COLOR, font=("Consolas", 14))
        self.lbl_potencia.pack(side=tk.LEFT, padx=20, pady=15)

        # Status das Vagas (Cards)
        vagas_frame = tk.Frame(center_frame, bg=BG_COLOR)
        vagas_frame.pack(fill=tk.X, pady=10)

        self.cards_vagas = {}
        for i in range(1, 5):
            card = tk.Frame(vagas_frame, bg=PANEL_COLOR, bd=1, relief=tk.SOLID, highlightbackground=ACCENT_COLOR, highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            lbl_tit = tk.Label(card, text=f"VAGA {i}", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 12, "bold"))
            lbl_tit.pack(pady=10)
            
            lbl_status = tk.Label(card, text="LIVRE", bg=PANEL_COLOR, fg=TEXT_MUTED, font=("Segoe UI", 10))
            lbl_status.pack(pady=5)
            
            self.cards_vagas[str(i)] = {"frame": card, "status": lbl_status}

        # TERMINAL DE LOGS
        log_frame = tk.Frame(center_frame, bg=PANEL_COLOR)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        lbl_log = tk.Label(log_frame, text="TERMINAL DE EVENTOS (OCPP & IA)", bg=PANEL_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10, "bold"))
        lbl_log.pack(anchor=tk.W, padx=10, pady=5)

        self.txt_log = tk.Text(log_frame, bg="#000000", fg="#00FF00", font=("Consolas", 10), state=tk.DISABLED, relief=tk.FLAT)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    # REGRAS DE NEGÓCIO E ATUALIZAÇÃO 
    def log_mensagem(self, msg, cor="#00FF00"):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def simular_log_ocpp(self, tipo, payload):
        frame = [2, f"msg_{random.randint(1000, 9999)}", tipo, payload]
        self.log_mensagem(f"OCPP: {json.dumps(frame)}", TEXT_MUTED)

    def atualizar_estado_sistema(self):
        # Simula Solar
        if 7 <= self.hora_simulada <= 17:
            self.geracao_solar = round(random.uniform(5.0, 10.0) if 10 <= self.hora_simulada <= 14 else random.uniform(1.0, 4.0), 2)
        else:
            self.geracao_solar = 0.0

        potencia_total = LIMITE_POTENCIA_HUB + self.geracao_solar

        self.lbl_hora.config(text=f"🕒 Hora: {self.hora_simulada:02d}:00")
        self.lbl_solar.config(text=f"☀️ Solar: {self.geracao_solar} kW")
        self.lbl_potencia.config(text=f"⚡ Disp: {potencia_total:.2f} kW")

        # Atualiza UI das Vagas
        for vid, card in self.cards_vagas.items():
            if vid in self.vagas:
                dados = self.vagas[vid]
                card["status"].config(text=f"OCUPADA\nCarga: {dados['soc']}%\nEnergia: {dados['energia_recarregada']:.2f} kWh", fg=SUCCESS_COLOR)
                card["frame"].config(highlightbackground=SUCCESS_COLOR)
            else:
                card["status"].config(text="LIVRE\n-\n-", fg=TEXT_MUTED)
                card["frame"].config(highlightbackground=ACCENT_COLOR)

    # AÇÕES DOS BOTÕES (POPUPS E LÓGICA)
    def avancar_tempo(self):
        self.hora_simulada = (self.hora_simulada + 1) % 24
        self.atualizar_estado_sistema()
        self.log_mensagem(f"⏳ Tempo avançado para {self.hora_simulada:02d}:00.")

    def popup_conectar_veiculo(self):
        if len(self.vagas) >= 4:
            messagebox.showwarning("Aviso", "Estação Lotada! Nenhuma vaga disponível.")
            return

        vaga_id = str(len(self.vagas) + 1)
        
        # Encontra a primeira vaga vazia
        for i in range(1, 5):
            if str(i) not in self.vagas:
                vaga_id = str(i)
                break

        popup = tk.Toplevel(self.root)
        popup.title(f"Conectar Vaga {vaga_id}")
        popup.geometry("300x200")
        popup.configure(bg=PANEL_COLOR)

        tk.Label(popup, text=f"Nova Sessão - Vaga {vaga_id}", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 12, "bold")).pack(pady=10)
        tk.Label(popup, text="Capacidade da Bateria (kWh):", bg=PANEL_COLOR, fg=TEXT_COLOR).pack()
        
        entry_cap = tk.Entry(popup, justify="center")
        entry_cap.pack(pady=5)
        entry_cap.insert(0, "40.0")

        def confirmar():
            try:
                cap = float(entry_cap.get())
                if cap <= 0: raise ValueError
                
                self.vagas[vaga_id] = {
                    "capacidade": cap,
                    "hora_inicio": self.hora_simulada,
                    "energia_recarregada": 0.0,
                    "soc": 0
                }
                self.atualizar_estado_sistema()
                self.simular_log_ocpp("StartTransaction", {"connectorId": int(vaga_id), "meterStart": 0})
                self.log_mensagem(f"Veículo conectado na Vaga {vaga_id} (Capacidade: {cap}kWh).", SUCCESS_COLOR)
                popup.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Insira um valor numérico válido maior que zero.")

        tk.Button(popup, text="Conectar", bg=ACCENT_COLOR, fg=TEXT_COLOR, relief=tk.FLAT, command=confirmar).pack(pady=15)

    def simular_ciclo_recarga(self):
        if not self.vagas:
            messagebox.showinfo("Info", "Nenhum veículo conectado.")
            return

        potencia_total = LIMITE_POTENCIA_HUB + self.geracao_solar
        if len(self.vagas) * POTENCIA_NOMINAL_VAGA > potencia_total:
            pot_vaga = potencia_total / len(self.vagas)
            self.log_mensagem(f"⚠️ SMART CHARGING: Potência limitada a {pot_vaga:.2f}kW por veículo.", ACCENT_COLOR)
        else:
            pot_vaga = POTENCIA_NOMINAL_VAGA

        for vid, dados in self.vagas.items():
            if dados["soc"] < 100:
                dados["energia_recarregada"] = min(dados["energia_recarregada"] + (pot_vaga * 0.2), dados["capacidade"])
                dados["soc"] = int((dados["energia_recarregada"] / dados["capacidade"]) * 100)
                self.simular_log_ocpp("MeterValues", {"connectorId": int(vid), "value": f"{dados['energia_recarregada']:.2f} kWh"})

        self.atualizar_estado_sistema()
        self.log_mensagem("⚡ Ciclo de recarga simulado com sucesso.")

    def acionar_ia(self):
        qtd = len(self.vagas)
        self.log_mensagem("🤖 INICIANDO ANÁLISE DE IA PREDITIVA...", "#FCA311")
        
        if self.geracao_solar > 5.0:
            self.log_mensagem("☀️ INSIGHT: Alta geração solar! Maximize o carregamento agora para energia custo zero.", "#FCA311")
        
        if qtd >= 3:
            self.log_mensagem("⚠️ ALERTA: Estação próxima à saturação. Smart Charging em prontidão.", "#FCA311")
        elif qtd > 0:
            self.log_mensagem("💡 INSIGHT: Rede operando com estabilidade térmica e energética.", "#FCA311")
        else:
            self.log_mensagem("💡 INSIGHT: Estação ociosa. Sugestão: Aplicar tarifa promocional no app.", "#FCA311")

    # MÓDULO DE PAGAMENTO
    def popup_pagamento(self):
        if not self.vagas:
            messagebox.showinfo("Info", "Não há sessões ativas para encerrar.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Pagamento e Liberação")
        popup.geometry("350x450")
        popup.configure(bg=PANEL_COLOR)

        tk.Label(popup, text="CAIXA REECHARGE", bg=PANEL_COLOR, fg=ACCENT_COLOR, font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        tk.Label(popup, text="Selecione a vaga para encerrar:", bg=PANEL_COLOR, fg=TEXT_COLOR).pack()
        vaga_var = tk.StringVar(popup)
        vaga_var.set(list(self.vagas.keys())[0])
        dropdown = ttk.Combobox(popup, textvariable=vaga_var, values=list(self.vagas.keys()), state="readonly", justify="center")
        dropdown.pack(pady=5)

        info_frame = tk.Frame(popup, bg=BG_COLOR, padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        lbl_resumo = tk.Label(info_frame, text="Aguardando seleção...", bg=BG_COLOR, fg=TEXT_COLOR, justify=tk.LEFT)
        lbl_resumo.pack()

        def atualizar_resumo(*args):
            vid = vaga_var.get()
            if vid in self.vagas:
                dados = self.vagas[vid]
                tarifa = TARIFA_BASE_COMERCIAL * (1.3 if 18 <= dados["hora_inicio"] <= 21 else 1.0)
                custo = dados["energia_recarregada"] * tarifa
                texto = f"Vaga: {vid}\nEnergia: {dados['energia_recarregada']:.2f} kWh\nTarifa: R$ {tarifa:.2f}/kWh\n\nTOTAL A PAGAR: R$ {custo:.2f}"
                lbl_resumo.config(text=texto, font=("Segoe UI", 11, "bold"))
                return custo, tarifa

        vaga_var.trace("w", atualizar_resumo)
        atualizar_resumo()

        def processar_pagamento(metodo):
            vid = vaga_var.get()
            custo, tarifa = atualizar_resumo()
            energia = self.vagas[vid]['energia_recarregada']

            self.historico_geral.append({
                "vaga": vid,
                "energia_kwh": round(energia, 2),
                "total_rs": round(custo, 2),
                "pagamento": metodo,
                "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            self.simular_log_ocpp("StopTransaction", {"connectorId": int(vid), "meterStop": int(energia)})
            del self.vagas[vid]
            self.atualizar_estado_sistema()
            
            self.log_mensagem(f"💳 PAGAMENTO APROVADO via {metodo}. Vaga {vid} liberada! Receita: R${custo:.2f}", SUCCESS_COLOR)
            messagebox.showinfo("Sucesso", f"Pagamento de R$ {custo:.2f} via {metodo} realizado com sucesso!\nRecibo emitido.")
            popup.destroy()

        tk.Label(popup, text="Forma de Pagamento:", bg=PANEL_COLOR, fg=TEXT_MUTED).pack(pady=(10,0))
        
        btn_pix = tk.Button(popup, text="❖ PIX", bg="#32BCAD", fg="#000000", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=lambda: processar_pagamento("PIX"))
        btn_pix.pack(fill=tk.X, padx=40, pady=5)

        btn_cartao = tk.Button(popup, text="💳 Cartão de Crédito", bg="#F4A261", fg="#000000", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=lambda: processar_pagamento("Cartão de Crédito"))
        btn_cartao.pack(fill=tk.X, padx=40, pady=5)

    def exportar_sair(self):
        if self.historico_geral:
            nome_arquivo = f"relatorio_financeiro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.historico_geral, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportado", f"Relatório financeiro salvo como:\n{nome_arquivo}")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReechargeGUI(root)
    root.mainloop()
