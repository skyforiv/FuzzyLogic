import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt
from skfuzzy import control as ctrl

#Değişkenlerin tanımlanması
hava_koşulları = ctrl.Antecedent(np.arange(0, 11, 1), 'hava_koşulları')
trafik_yoğunluğu = ctrl.Antecedent(np.arange(0, 11, 1), 'trafik_yoğunluğu')
rötar_olasılığı = ctrl.Consequent(np.arange(0, 101, 1), 'rötar_olasılığı')

#Üyelik fonksiyonlarının tanımlanması
hava_koşulları.automf(3, names=['kötü', 'ortalama', 'iyi'])
trafik_yoğunluğu.automf(3, names=['düşük', 'orta', 'yüksek'])
rötar_olasılığı['düşük'] = fuzz.trimf(rötar_olasılığı.universe, [0, 0, 50])
rötar_olasılığı['orta'] = fuzz.trimf(rötar_olasılığı.universe, [0, 50, 100])
rötar_olasılığı['yüksek'] = fuzz.trimf(rötar_olasılığı.universe, [50, 100, 100])

#Kuralların tanımlanması
kurallar = [
    ctrl.Rule(hava_koşulları['kötü'] & trafik_yoğunluğu['yüksek'], rötar_olasılığı['yüksek']),
    ctrl.Rule(hava_koşulları['kötü'] & trafik_yoğunluğu['orta'], rötar_olasılığı['yüksek']),
    ctrl.Rule(hava_koşulları['kötü'] & trafik_yoğunluğu['düşük'], rötar_olasılığı['orta']),
    ctrl.Rule(hava_koşulları['ortalama'] & trafik_yoğunluğu['yüksek'], rötar_olasılığı['yüksek']),
    ctrl.Rule(hava_koşulları['ortalama'] & trafik_yoğunluğu['orta'], rötar_olasılığı['orta']),
    ctrl.Rule(hava_koşulları['ortalama'] & trafik_yoğunluğu['düşük'], rötar_olasılığı['düşük']),
    ctrl.Rule(hava_koşulları['iyi'] & trafik_yoğunluğu['yüksek'], rötar_olasılığı['orta']),
    ctrl.Rule(hava_koşulları['iyi'] & trafik_yoğunluğu['orta'], rötar_olasılığı['düşük']),
    ctrl.Rule(hava_koşulları['iyi'] & trafik_yoğunluğu['düşük'], rötar_olasılığı['düşük'])
]

rötar_ctrl = ctrl.ControlSystem(kurallar)
rötar_derecesi = ctrl.ControlSystemSimulation(rötar_ctrl)

#Girdilerin atanması ve çıktının hesaplanması
rötar_derecesi.input['hava_koşulları'] = 3    #Örneğin, hava koşulları için 3
rötar_derecesi.input['trafik_yoğunluğu'] = 8  #Örneğin, trafik yoğunluğu için 8
rötar_derecesi.compute()

#Çıktının görüntülenmesi
print("Rötar olasılığı:", rötar_derecesi.output['rötar_olasılığı'])

rötar_olasılığı.view(sim=rötar_derecesi)

plt.show()
