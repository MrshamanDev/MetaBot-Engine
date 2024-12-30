import sys
import time
import psutil
import random
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit,
    QLabel, QMessageBox, QProgressBar, QHBoxLayout, QSpinBox,
    QTabWidget, QTextEdit, QComboBox, QCheckBox, QGroupBox, QGridLayout,
    QFileDialog
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QColor, QIcon
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

class PerformanceMonitor(QThread):
    update_signal = pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            network_usage /= 1024 * 1024  # Convert to MB
            self.update_signal.emit(cpu_usage, memory_usage, network_usage)
            time.sleep(1)

    def stop(self):
        self.running = False

class PerformanceGraph(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.cpu_data = []
        self.memory_data = []
        self.network_data = []

    def update_graph(self, cpu, memory, network):
        self.cpu_data.append(cpu)
        self.memory_data.append(memory)
        self.network_data.append(network)
        if len(self.cpu_data) > 60:
            self.cpu_data.pop(0)
            self.memory_data.pop(0)
            self.network_data.pop(0)
        self.axes.clear()
        self.axes.plot(self.cpu_data, label='CPU')
        self.axes.plot(self.memory_data, label='Memory')
        self.axes.plot(self.network_data, label='Network')
        self.axes.legend()
        self.axes.set_ylim(0, 100)
        self.axes.set_title('Performance Monitoring')
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Usage (%)')
        self.draw()

class HumanLikeBot(QThread):
    log = pyqtSignal(str)
    update_counts = pyqtSignal(int, int, float)

    def __init__(self, url, tab_count, proxies=None, view_duration=(5, 15), headless=True, performance_settings=None, traffic_sources=None):
        super().__init__()
        self.url = url
        self.running = True
        self.total_runs = 0
        self.finished_runs = 0
        self.tab_count = tab_count
        self.proxies = proxies or []
        self.view_duration = view_duration
        self.user_agent = UserAgent()
        self.headless = headless
        self.performance_settings = performance_settings or {}
        self.traffic_sources = traffic_sources or ['direct']

    def run(self):
        logging.info("Bot started running")
        try:
            service = Service(ChromeDriverManager().install())
            while self.running:
                self.total_runs += 1
                start_ram = psutil.virtual_memory().percent
                self.open_tab(service)
                self.finished_runs += 1
                end_ram = psutil.virtual_memory().percent
                ram_usage = end_ram - start_ram
                self.update_counts.emit(self.total_runs, self.finished_runs, ram_usage)
                self.log.emit(f"Visitor {self.total_runs} send")
                time.sleep(random.uniform(1, 5))
        except Exception as e:
            logging.error(f"Error in bot run: {str(e)}")

    def setup_chrome_options(self, proxy=None):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        
        if self.performance_settings.get('disable_images', False):
            options.add_argument("--blink-settings=imagesEnabled=false")
        
        prefs = {
            "profile.managed_default_content_settings.images": 2 if self.performance_settings.get('disable_images', False) else 1,
            "profile.managed_default_content_settings.javascript": 2 if self.performance_settings.get('disable_javascript', False) else 1,
            "profile.managed_default_content_settings.cookies": 2,
            "profile.managed_default_content_settings.plugins": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)
        
        options.add_argument(f'user-agent={self.user_agent.random}')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        return options

    def open_tab(self, service):
        try:
            proxy = random.choice(self.proxies) if self.proxies else None
            options = self.setup_chrome_options(proxy)
            driver = webdriver.Chrome(service=service, options=options)
            if self.performance_settings.get('clear_cache', False):
                self.optimize_performance(driver)
            self.log.emit(f"Opening new tab: {self.url}")
            if 'direct' not in self.traffic_sources or (len(self.traffic_sources) > 1 and random.choice([True, False])):
                self.simulate_traffic_source(driver)
            else:
                driver.get(self.url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            self.simulate_human_behavior(driver)
            time.sleep(random.uniform(*self.view_duration))
            driver.quit()
        except Exception as e:
            logging.error(f"Error in tab: {str(e)}")

    def simulate_human_behavior(self, driver):
        # Scroll behavior
        for _ in range(random.randint(3, 8)):
            driver.execute_script(f"window.scrollTo(0, {random.randint(100, 1000)});")
            time.sleep(random.uniform(0.5, 2.0))

        # Click random links
        links = driver.find_elements(By.TAG_NAME, "a")
        for _ in range(random.randint(1, 3)):
            if links:
                link = random.choice(links)
                try:
                    ActionChains(driver).move_to_element(link).pause(random.uniform(0.1, 0.3)).click().perform()
                    time.sleep(random.uniform(2, 5))
                    driver.back()
                except:
                    pass

        # Simulate mouse movements
        for _ in range(random.randint(5, 10)):
            x = random.randint(0, driver.execute_script("return window.innerWidth;"))
            y = random.randint(0, driver.execute_script("return window.innerHeight;"))
            ActionChains(driver).move_by_offset(x, y).perform()
            time.sleep(random.uniform(0.1, 0.5))

    def stop(self):
        self.running = False
        self.log.emit("Stopping bot...")

    def simulate_traffic_source(self, driver):
        traffic_source = random.choice(self.traffic_sources)
        if traffic_source == 'search_engine':
            search_engines = [
                "https://www.google.com",
                "https://www.bing.com",
                "https://www.yahoo.com",
                "https://duckduckgo.com"
            ]
            source = random.choice(search_engines)
            driver.get(source)
            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(self.url)
            search_box.send_keys(Keys.RETURN)
        elif traffic_source == 'social_media':
            social_media = [
                "https://www.facebook.com",
                "https://www.twitter.com",
                "https://www.linkedin.com",
                "https://www.reddit.com"
            ]
            source = random.choice(social_media)
            driver.get(source)
        else:  # Referral or other sources
            referral_sites = [
                "https://www.example.com",
                "https://www.randomwebsite.com",
                "https://www.blogspot.com"
            ]
            source = random.choice(referral_sites)
            driver.get(source)
        
        time.sleep(random.uniform(1, 3))
        driver.execute_script(f"window.location.href = '{self.url}';")
        
        # Set a custom referrer
        driver.execute_script(f"Object.defineProperty(document, 'referrer', {{get : function(){{ return '{source}'}}}});")

    def optimize_performance(self, driver):
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.execute_script("window.indexedDB.deleteDatabase(null);")
        driver.execute_script("caches.keys().then(function(cacheNames) {return Promise.all(cacheNames.map(function(cacheName){return caches.delete(cacheName)}))}).then(function(){console.log('Cache cleared')});")

class AdvancedViewBot(QWidget):
    def __init__(self):
        super().__init__()
        self.total_runs = 0
        self.finished_runs = 0
        self.proxies = []
        self.bot = None
        self.dark_mode = False
        self.performance_monitor = None
        self.init_ui()
        self.setup_logging()

    def init_ui(self):
        self.setWindowTitle("Advanced Human-like View Bot")
        self.setGeometry(100, 100, 1000, 800)
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_main_tab(), "Main")
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        self.tabs.addTab(self.create_performance_tab(), "Performance")
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_run_count_and_ram)
        self.timer.start(1000)

    def create_main_tab(self):
        main_widget = QWidget()
        layout = QVBoxLayout()

        url_layout = QHBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://example.com")
        url_layout.addWidget(QLabel("Website URL:"))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        tab_layout = QHBoxLayout()
        self.tab_count_input = QSpinBox(self)
        self.tab_count_input.setRange(1, 50)
        self.tab_count_input.setValue(1)
        tab_layout.addWidget(QLabel("Number of Tabs:"))
        tab_layout.addWidget(self.tab_count_input)
        layout.addLayout(tab_layout)

        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_bot)
        self.run_button.setStyleSheet("background-color: #4CAF50; color: white;")
        button_layout.addWidget(self.run_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("background-color: #f44336; color: white;")
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.ram_usage_label = QLabel("RAM Usage: 0%")
        layout.addWidget(self.ram_usage_label)

        self.console_box = QTextEdit(self)
        self.console_box.setReadOnly(True)
        self.console_box.setStyleSheet("background-color: #2b2b2b; color: #f0f0f0;")
        layout.addWidget(QLabel("Console:"))
        layout.addWidget(self.console_box)

        layout.addWidget(self.create_footer())

        main_widget.setLayout(layout)
        return main_widget

    def create_settings_tab(self):
        settings_widget = QWidget()
        layout = QVBoxLayout()

        proxy_group = QGroupBox("Proxy Settings")
        proxy_layout = QVBoxLayout()
        self.proxy_input = QLineEdit(self)
        self.proxy_input.setPlaceholderText("Proxy (optional): ip:port")
        proxy_layout.addWidget(self.proxy_input)
        self.proxy_file_button = QPushButton("Select Proxy File", self)
        self.proxy_file_button.clicked.connect(self.select_proxy_file)
        proxy_layout.addWidget(self.proxy_file_button)
        self.proxy_file_label = QLabel("No proxy file selected")
        proxy_layout.addWidget(self.proxy_file_label)
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)

        view_duration_group = QGroupBox("View Duration")
        view_duration_layout = QGridLayout()
        self.min_duration = QSpinBox(self)
        self.min_duration.setRange(1, 3600)
        self.min_duration.setValue(5)
        self.max_duration = QSpinBox(self)
        self.max_duration.setRange(1, 3600)
        self.max_duration.setValue(15)
        self.duration_unit = QComboBox(self)
        self.duration_unit.addItems(["Seconds", "Minutes", "Hours"])
        view_duration_layout.addWidget(QLabel("Min:"), 0, 0)
        view_duration_layout.addWidget(self.min_duration, 0, 1)
        view_duration_layout.addWidget(QLabel("Max:"), 0, 2)
        view_duration_layout.addWidget(self.max_duration, 0, 3)
        view_duration_layout.addWidget(QLabel("Unit:"), 1, 0)
        view_duration_layout.addWidget(self.duration_unit, 1, 1, 1, 3)
        view_duration_group.setLayout(view_duration_layout)
        layout.addWidget(view_duration_group)

        traffic_source_group = QGroupBox("Traffic Source Simulation")
        traffic_source_layout = QVBoxLayout()
        self.traffic_source_checkboxes = {
            'direct': QCheckBox("Direct"),
            'search_engine': QCheckBox("Search Engine"),
            'social_media': QCheckBox("Social Media"),
            'referral': QCheckBox("Referral")
        }
        for checkbox in self.traffic_source_checkboxes.values():
            traffic_source_layout.addWidget(checkbox)
        traffic_source_group.setLayout(traffic_source_layout)
        layout.addWidget(traffic_source_group)

        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        layout.addWidget(self.dark_mode_checkbox)

        layout.addWidget(self.create_footer())

        settings_widget.setLayout(layout)
        return settings_widget

    def create_performance_tab(self):
        performance_widget = QWidget()
        layout = QVBoxLayout()

        self.performance_graph = PerformanceGraph(width=8, height=4)
        layout.addWidget(self.performance_graph)

        self.cpu_label = QLabel("CPU Usage: 0%")
        self.memory_label = QLabel("Memory Usage: 0%")
        self.network_label = QLabel("Network Usage: 0 MB")
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.memory_label)
        layout.addWidget(self.network_label)

        layout.addWidget(self.create_footer())

        performance_widget.setLayout(layout)
        return performance_widget

    def create_footer(self):
        footer = QLabel("MetaBot Engine Programmed By Shaman Siddiqui")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #888; margin-top: 10px;")
        return footer

    def setup_logging(self):
        logging.basicConfig(
            filename='bot_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def select_proxy_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Proxy File", "", "Text Files (*.txt)")
        if file_name:
            self.proxy_file_label.setText(f"Selected proxy file: {file_name}")
            with open(file_name, 'r') as file:
                self.proxies = [line.strip() for line in file if line.strip()]
            self.proxy_input.setEnabled(False)
            self.proxy_input.setText("")
        else:
            self.proxy_file_label.setText("No proxy file selected")
            self.proxies = []
            self.proxy_input.setEnabled(True)

    def run_bot(self):
        try:
            url = self.url_input.text().strip()
            if not url:
                QMessageBox.warning(self, "Input Error", "Please enter a valid URL.")
                return

            tab_count = self.tab_count_input.value()
            if not self.proxies:
                proxy = self.proxy_input.text().strip() or None
                self.proxies = [proxy] if proxy else []

            view_duration = self.get_view_duration()

            if self.bot and self.bot.isRunning():
                QMessageBox.warning(self, "Bot Running", "Bot is already running.")
                return

            traffic_sources = [source for source, checkbox in self.traffic_source_checkboxes.items() if checkbox.isChecked()]
            
            self.bot = HumanLikeBot(url, tab_count, self.proxies, view_duration, traffic_sources=traffic_sources)
            self.bot.log.connect(self.update_console)
            self.bot.update_counts.connect(self.update_counts)
            self.bot.start()

            self.performance_monitor = PerformanceMonitor()
            self.performance_monitor.update_signal.connect(self.update_performance)
            self.performance_monitor.start()

            self.stop_button.setEnabled(True)
            self.run_button.setEnabled(False)
            logging.info(f"Bot started with URL: {url}, Tabs: {tab_count}, Proxies: {self.proxies}, View Duration: {view_duration}")
        except Exception as e:
            logging.error(f"Error starting bot: {str(e)}")
            QMessageBox.warning(self, "Error", f"Error starting bot: {str(e)}")

    def stop_bot(self):
        if self.bot:
            self.bot.stop()
            self.bot.wait()
        if self.performance_monitor:
            self.performance_monitor.stop()
            self.performance_monitor.wait()
        self.stop_button.setEnabled(False)
        self.run_button.setEnabled(True)
        logging.info("Bot stopped")

    def update_console(self, message):
        self.console_box.append(message)

    def update_counts(self, total, finished, ram_usage):
        self.total_runs = total
        self.finished_runs = finished
        self.progress_bar.setValue(int((finished / total) * 100))
        self.ram_usage_label.setText(f"RAM Usage: {ram_usage:.2f}%")

    def update_performance(self, cpu, memory, network):
        self.cpu_label.setText(f"CPU Usage: {cpu:.2f}%")
        self.memory_label.setText(f"Memory Usage: {memory:.2f}%")
        self.network_label.setText(f"Network Usage: {network:.2f} MB")
        self.performance_graph.update_graph(cpu, memory, network)

    def update_run_count_and_ram(self):
        ram_usage = psutil.virtual_memory().percent
        self.ram_usage_label.setText(f"RAM Usage: {ram_usage:.2f}%")

    def get_view_duration(self):
        min_duration = self.min_duration.value()
        max_duration = self.max_duration.value()
        unit = self.duration_unit.currentText()
        
        if unit == "Minutes":
            min_duration *= 60
            max_duration *= 60
        elif unit == "Hours":
            min_duration *= 3600
            max_duration *= 3600
        
        return (min_duration, max_duration)

    def toggle_dark_mode(self, state):
        self.dark_mode = state == Qt.Checked
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #2b2b2b; color: #f0f0f0; }
                QLineEdit, QSpinBox, QComboBox { background-color: #3b3b3b; color: #f0f0f0; border: 1px solid #555; }
                QPushButton { background-color: #4CAF50; color: white; border: none; padding: 5px; }
                QPushButton:disabled { background-color: #45a049; }
                QTableWidget { gridline-color: #3b3b3b; }
                QHeaderView::section { background-color: #3b3b3b; color: #f0f0f0; }
                QLabel[footer="true"] { color: #888; }
            """)
        else:
            self.setStyleSheet("")

    def closeEvent(self, event):
        if self.bot:
            self.bot.stop()
            self.bot.wait()
        if self.performance_monitor:
            self.performance_monitor.stop()
            self.performance_monitor.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Metabot.ico'))
    window = AdvancedViewBot()
    window.show()
    sys.exit(app.exec_())

