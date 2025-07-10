import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Dict, Any

class FabriCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("FabriCalc - Calculadora de Costos 3D")
        self.root.geometry("800x600")
        
        # Load configuration
        self.config_file = "config.json"
        self.load_config()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_calculator_tab()
        self.create_config_tab()
    
    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Error al cargar config.json")
                self.create_default_config()
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Create default configuration"""
        self.config = {
            "materiales": {
                "PLA Wood": 150000,
                "PETG": 120000,
                "PLA+": 90000
            },
            "electricidad_kwh": 968,
            "consumo_kw_por_hora": 0.5,
            "precio_impresora": 1200000,
            "vida_util_horas": 7000,
            "envio_local": 6000,
            "envio_nacional": 12000,
            "precio_hora_trabajo": 6471,
            "factor_desperdicio": 100
        }
        self.save_config()
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar config.json: {e}")
    
    def create_calculator_tab(self):
        """Create the calculator tab"""
        calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(calculator_frame, text="Calculadora")
        
        # Title
        title_label = ttk.Label(calculator_frame, text="Calculadora de Costos 3D", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.LabelFrame(calculator_frame, text="Datos de la Impresión", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Material selection
        ttk.Label(input_frame, text="Material:").grid(row=0, column=0, sticky='w', pady=2)
        self.material_var = tk.StringVar()
        self.material_combo = ttk.Combobox(input_frame, textvariable=self.material_var, 
                                          values=list(self.config["materiales"].keys()), state="readonly")
        self.material_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        self.material_combo.set(list(self.config["materiales"].keys())[0])
        
        # Weight input
        ttk.Label(input_frame, text="Peso (gramos):").grid(row=1, column=0, sticky='w', pady=2)
        self.weight_var = tk.StringVar(value="10")
        weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        weight_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Print time input - Hours and Minutes
        ttk.Label(input_frame, text="Tiempo de impresión:").grid(row=2, column=0, sticky='w', pady=2)
        
        time_frame = ttk.Frame(input_frame)
        time_frame.grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        
        self.print_hours_var = tk.StringVar(value="0")
        self.print_minutes_var = tk.StringVar(value="0")
        
        ttk.Label(time_frame, text="Horas:").pack(side='left')
        hours_entry = ttk.Entry(time_frame, textvariable=self.print_hours_var, width=8)
        hours_entry.pack(side='left', padx=(5,10))
        
        ttk.Label(time_frame, text="Minutos:").pack(side='left')
        minutes_entry = ttk.Entry(time_frame, textvariable=self.print_minutes_var, width=8)
        minutes_entry.pack(side='left', padx=(5,0))
        
        # Shipping type
        ttk.Label(input_frame, text="Tipo de envío:").grid(row=3, column=0, sticky='w', pady=2)
        self.shipping_var = tk.StringVar(value="Personal")
        shipping_combo = ttk.Combobox(input_frame, textvariable=self.shipping_var,
                                     values=["Personal", "Local", "Nacional"], state="readonly")
        shipping_combo.grid(row=3, column=1, sticky='ew', padx=5, pady=2)
        
        # Profit percentage
        ttk.Label(input_frame, text="Ganancia (%):").grid(row=4, column=0, sticky='w', pady=2)
        self.profit_var = tk.StringVar(value="40")
        profit_entry = ttk.Entry(input_frame, textvariable=self.profit_var)
        profit_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=2)
        
        # Post-processing time
        ttk.Label(input_frame, text="Post-procesado (minutos):").grid(row=5, column=0, sticky='w', pady=2)
        self.post_time_var = tk.StringVar(value="60")
        post_time_entry = ttk.Entry(input_frame, textvariable=self.post_time_var)
        post_time_entry.grid(row=5, column=1, sticky='ew', padx=5, pady=2)
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        # Calculate button
        calc_button = ttk.Button(calculator_frame, text="Calcular Precio", 
                                command=self.calculate_price)
        calc_button.pack(pady=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(calculator_frame, text="Resultados", padding=10)
        self.results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Results labels
        self.material_cost_label = ttk.Label(self.results_frame, text="Costo material: $0")
        self.material_cost_label.pack(anchor='w')
        
        self.electricity_cost_label = ttk.Label(self.results_frame, text="Costo electricidad: $0")
        self.electricity_cost_label.pack(anchor='w')
        
        self.depreciation_cost_label = ttk.Label(self.results_frame, text="Depreciación máquina: $0")
        self.depreciation_cost_label.pack(anchor='w')
        
        self.labor_cost_label = ttk.Label(self.results_frame, text="Costo trabajo: $0")
        self.labor_cost_label.pack(anchor='w')
        
        self.shipping_cost_label = ttk.Label(self.results_frame, text="Costo envío: $0")
        self.shipping_cost_label.pack(anchor='w')
        
        self.total_cost_label = ttk.Label(self.results_frame, text="Costo total: $0", 
                                         font=('Arial', 12, 'bold'))
        self.total_cost_label.pack(anchor='w', pady=(10,0))
        
        self.final_price_label = ttk.Label(self.results_frame, text="Precio final: $0", 
                                          font=('Arial', 14, 'bold'))
        self.final_price_label.pack(anchor='w')
    
    def create_config_tab(self):
        """Create the configuration tab"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuración")
        
        # Title
        title_label = ttk.Label(config_frame, text="Configuración del Sistema", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Create scrollable frame
        canvas = tk.Canvas(config_frame)
        scrollbar = ttk.Scrollbar(config_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Materials section
        materials_frame = ttk.LabelFrame(scrollable_frame, text="Materiales (COP/kg)", padding=10)
        materials_frame.pack(fill='x', padx=10, pady=5)
        
        self.material_entries = {}
        for i, (material, price) in enumerate(self.config["materiales"].items()):
            ttk.Label(materials_frame, text=f"{material}:").grid(row=i, column=0, sticky='w', pady=2)
            var = tk.StringVar(value=str(price))
            entry = ttk.Entry(materials_frame, textvariable=var, width=15)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.material_entries[material] = var
        
        # Add new material
        ttk.Label(materials_frame, text="Nuevo material:").grid(row=len(self.config["materiales"]), column=0, sticky='w', pady=2)
        self.new_material_var = tk.StringVar()
        new_material_entry = ttk.Entry(materials_frame, textvariable=self.new_material_var, width=15)
        new_material_entry.grid(row=len(self.config["materiales"]), column=1, padx=5, pady=2)
        
        ttk.Label(materials_frame, text="Precio:").grid(row=len(self.config["materiales"]), column=2, sticky='w', pady=2)
        self.new_price_var = tk.StringVar()
        new_price_entry = ttk.Entry(materials_frame, textvariable=self.new_price_var, width=15)
        new_price_entry.grid(row=len(self.config["materiales"]), column=3, padx=5, pady=2)
        
        add_button = ttk.Button(materials_frame, text="Agregar Material", 
                               command=self.add_material)
        add_button.grid(row=len(self.config["materiales"]), column=4, padx=5, pady=2)
        
        # Other settings
        settings_frame = ttk.LabelFrame(scrollable_frame, text="Configuración General", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=5)
        
        # Electricity settings
        ttk.Label(settings_frame, text="Precio electricidad (COP/kWh):").grid(row=0, column=0, sticky='w', pady=2)
        self.electricity_var = tk.StringVar(value=str(self.config["electricidad_kwh"]))
        electricity_entry = ttk.Entry(settings_frame, textvariable=self.electricity_var)
        electricity_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Consumo (kW/hora):").grid(row=1, column=0, sticky='w', pady=2)
        self.consumption_var = tk.StringVar(value=str(self.config["consumo_kw_por_hora"]))
        consumption_entry = ttk.Entry(settings_frame, textvariable=self.consumption_var)
        consumption_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=2)
        
        # Printer settings
        ttk.Label(settings_frame, text="Precio impresora (COP):").grid(row=2, column=0, sticky='w', pady=2)
        self.printer_price_var = tk.StringVar(value=str(self.config["precio_impresora"]))
        printer_price_entry = ttk.Entry(settings_frame, textvariable=self.printer_price_var)
        printer_price_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Vida útil (horas):").grid(row=3, column=0, sticky='w', pady=2)
        self.life_hours_var = tk.StringVar(value=str(self.config["vida_util_horas"]))
        life_hours_entry = ttk.Entry(settings_frame, textvariable=self.life_hours_var)
        life_hours_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=2)
        
        # Shipping settings
        ttk.Label(settings_frame, text="Envío local (COP):").grid(row=4, column=0, sticky='w', pady=2)
        self.local_shipping_var = tk.StringVar(value=str(self.config["envio_local"]))
        local_shipping_entry = ttk.Entry(settings_frame, textvariable=self.local_shipping_var)
        local_shipping_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=2)
        
        ttk.Label(settings_frame, text="Envío nacional (COP):").grid(row=5, column=0, sticky='w', pady=2)
        self.national_shipping_var = tk.StringVar(value=str(self.config["envio_nacional"]))
        national_shipping_entry = ttk.Entry(settings_frame, textvariable=self.national_shipping_var)
        national_shipping_entry.grid(row=5, column=1, sticky='ew', padx=5, pady=2)
        
        # Labor cost
        ttk.Label(settings_frame, text="Precio hora trabajo (COP):").grid(row=6, column=0, sticky='w', pady=2)
        self.labor_price_var = tk.StringVar(value=str(self.config["precio_hora_trabajo"]))
        labor_price_entry = ttk.Entry(settings_frame, textvariable=self.labor_price_var)
        labor_price_entry.grid(row=6, column=1, sticky='ew', padx=5, pady=2)
        
        # Waste factor
        ttk.Label(settings_frame, text="Factor desperdicio (%):").grid(row=7, column=0, sticky='w', pady=2)
        self.waste_factor_var = tk.StringVar(value=str(self.config["factor_desperdicio"]))
        waste_factor_entry = ttk.Entry(settings_frame, textvariable=self.waste_factor_var)
        waste_factor_entry.grid(row=7, column=1, sticky='ew', padx=5, pady=2)
        
        # Configure grid weights
        settings_frame.columnconfigure(1, weight=1)
        
        # Save and Reset buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=10)
        
        save_button = ttk.Button(button_frame, text="Guardar Configuración", 
                                command=self.save_configuration)
        save_button.pack(side='left', padx=(0,10))
        
        reset_button = ttk.Button(button_frame, text="Reiniciar Valores", 
                                 command=self.reset_configuration)
        reset_button.pack(side='left')
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_material(self):
        """Add a new material to the configuration"""
        material = self.new_material_var.get().strip()
        price = self.new_price_var.get().strip()
        
        if not material or not price:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos")
            return
        
        try:
            price_float = float(price)
            self.config["materiales"][material] = price_float
            self.save_config()
            self.refresh_materials()
            self.new_material_var.set("")
            self.new_price_var.set("")
            messagebox.showinfo("Éxito", f"Material '{material}' agregado")
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido")
    
    def refresh_materials(self):
        """Refresh materials in the calculator tab"""
        self.material_combo['values'] = list(self.config["materiales"].keys())
        if self.material_combo.get() not in self.config["materiales"]:
            self.material_combo.set(list(self.config["materiales"].keys())[0])
    
    def save_configuration(self):
        """Save all configuration changes"""
        try:
            # Update materials
            for material, var in self.material_entries.items():
                self.config["materiales"][material] = float(var.get())
            
            # Update other settings
            self.config["electricidad_kwh"] = float(self.electricity_var.get())
            self.config["consumo_kw_por_hora"] = float(self.consumption_var.get())
            self.config["precio_impresora"] = float(self.printer_price_var.get())
            self.config["vida_util_horas"] = float(self.life_hours_var.get())
            self.config["envio_local"] = float(self.local_shipping_var.get())
            self.config["envio_nacional"] = float(self.national_shipping_var.get())
            self.config["precio_hora_trabajo"] = float(self.labor_price_var.get())
            self.config["factor_desperdicio"] = float(self.waste_factor_var.get())
            
            self.save_config()
            self.refresh_materials()
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {e}")
    
    def reset_configuration(self):
        """Reset configuration to default values"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres reiniciar todos los valores a los predeterminados?"):
            self.create_default_config()
            self.load_config()
            self.refresh_materials()
            messagebox.showinfo("Éxito", "Valores reiniciados correctamente")
    
    def calculate_price(self):
        """Calculate the final price"""
        try:
            # Get input values
            material = self.material_var.get()
            weight = float(self.weight_var.get()) / 1000  # Convert to kg
            
            # Calculate print time from hours and minutes
            print_hours = float(self.print_hours_var.get())
            print_minutes = float(self.print_minutes_var.get())
            print_time = print_hours + (print_minutes / 60)
            
            shipping_type = self.shipping_var.get()
            profit_percent = float(self.profit_var.get()) / 100
            post_time = float(self.post_time_var.get()) / 60  # Convert to hours
            
            # Calculate costs
            waste_factor = 1 + (self.config["factor_desperdicio"] / 100)
            material_cost = weight * waste_factor * self.config["materiales"][material]
            electricity_cost = print_time * self.config["consumo_kw_por_hora"] * self.config["electricidad_kwh"]
            depreciation_cost = (print_time / self.config["vida_util_horas"]) * self.config["precio_impresora"]
            labor_cost = ((print_time/2) + post_time) * self.config["precio_hora_trabajo"]
            
            # Shipping cost
            if shipping_type == "Personal":
                shipping_cost = 0
            elif shipping_type == "Local":
                shipping_cost = self.config["envio_local"]
            else:  # Nacional
                shipping_cost = self.config["envio_nacional"]
            
            # Total cost
            total_cost = material_cost + electricity_cost + depreciation_cost + labor_cost + shipping_cost
            
            # Final price with profit
            final_price = total_cost * (1 + profit_percent)
            
            # Update labels
            self.material_cost_label.config(text=f"Costo material: ${material_cost:,.0f}")
            self.electricity_cost_label.config(text=f"Costo electricidad: ${electricity_cost:,.0f}")
            self.depreciation_cost_label.config(text=f"Uso de la máquina: ${depreciation_cost:,.0f}")
            self.labor_cost_label.config(text=f"Costo trabajo: ${labor_cost:,.0f}")
            self.shipping_cost_label.config(text=f"Costo envío: ${shipping_cost:,.0f}")
            self.total_cost_label.config(text=f"Costo total: ${total_cost:,.0f}")
            self.final_price_label.config(text=f"Precio final: ${final_price:,.0f}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Por favor verifica que todos los campos numéricos sean válidos")
        except KeyError:
            messagebox.showerror("Error", "Material no encontrado en la configuración")

def main():
    root = tk.Tk()
    app = FabriCalc(root)
    root.mainloop()

if __name__ == "__main__":
    main() 