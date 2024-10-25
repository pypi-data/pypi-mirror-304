import nvidia_smi
import os
import time
import threading
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import psutil
import warnings
import functools

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")


def hardware_metrics(path='./hardware_metrics_results'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def get_gpu_info():
                nvidia_smi.nvmlInit()
                deviceCount = nvidia_smi.nvmlDeviceGetCount()
                for i in range(deviceCount):
                    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                    util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                    mem = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
                    ram = psutil.virtual_memory()
                    cpu_util = psutil.cpu_percent()

                    return {'gpu-mem-used': (mem.total-mem.free)/1024**3, 'gpu-util': util.gpu, 
                            'ram-mem-used': (ram.used)/1024**3, 'cpu-util': cpu_util}
            
            def display():
                
                while not func_ended:
                    values.append(get_gpu_info())
                    time.sleep(1)

            def calculate_final_metrics(values):
                
                gpu_mems = [x['gpu-mem-used'] for x in values]
                gpu_utils = [x['gpu-util'] for x in values]

                ram_mems = [x['ram-mem-used'] for x in values]
                cpu_utils = [x['cpu-util'] for x in values]

                def stats(lista):
                    return (np.mean(lista), np.median(lista), np.std(lista))

                gpu_mem_stats = stats(gpu_mems)
                gpu_util_stats = stats(gpu_utils)

                ram_mem_stats = stats(ram_mems)
                cpu_util_stats = stats(cpu_utils)

                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
                gpu_total = nvidia_smi.nvmlDeviceGetMemoryInfo(handle).total/1024**3
                ram_total = psutil.virtual_memory().total/1024**3

                def plot_percent(lista, titulo):
                    sns.lineplot(lista)
                    plt.title(titulo)
                    plt.xlabel('Segundos')
                    plt.ylabel('% de uso')
                    plt.ylim((0, 100))
                    plt.savefig(path+'/'+titulo+'.png')

                def plot_memory(lista, titulo, total_memory):
                    sns.lineplot(lista)
                    plt.title(titulo)
                    plt.xlabel('Segundos')
                    plt.ylabel('GB')
                    plt.ylim((0, total_memory))
                    plt.savefig(path+'/'+titulo+'.png')
                

                
                plot_percent(gpu_utils,'Uso de GPU')
                plt.close()
                plot_percent(cpu_utils,'Uso de CPU')
                plt.close()
                plot_memory(gpu_mems,'Memoria de GPU', gpu_total)
                plt.close()
                plot_memory(ram_mems,'Memoria RAM', ram_total)

                final_dict = {'VRAM [GB]': gpu_mem_stats, 'GPU[%]': gpu_util_stats, 'RAM[GB]': ram_mem_stats, 'CPU[%]': cpu_util_stats}
                
                return final_dict



            values=[]
            func_ended=False
            
            t_start = time.time()
            x = threading.Thread(target=display, daemon=True)
            x.start()

            res = func(*args, **kwargs)
            t_end = time.time()
            total_time = t_end - t_start

            func_ended=True

            if not os.path.isdir(path):
                    os.makedirs(path)

            total_metrics = calculate_final_metrics(values)

            with open(path+'/stats.txt', 'w+') as f:
                
                for name, metrics in total_metrics.items():
                    f.write(name+':\n')
                    f.write(f'Media: {metrics[0]}\n')
                    f.write(f'Mediana: {metrics[1]}\n')
                    f.write(f'Desviacón típica: {metrics[2]}\n\n')
                
                f.write(f'\nTiempo total [s]: {total_time}')

            return res
        return wrapper
    return decorator