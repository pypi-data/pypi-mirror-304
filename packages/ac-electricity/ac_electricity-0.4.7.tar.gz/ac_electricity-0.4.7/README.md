## acelectricity module
 
The aim of this project is to understand the rudiments of linear AC electrical circuits and their functioning.  

### Prerequisites

Python : version 3    
All operating systems  
Libraries :   
- numpy  
- matplotlib.pyplot  
- matplotlib.widgets  

### Installing acelectricity python module

From Pypi repository :  
[https://pypi.org/project/ac-electricity](https://pypi.org/project/ac-electricity)


```
pip install ac-electricity
```

### Basic electrical quantities

- Voltage (volt)
- Current (ampere)
- Impedance Z (ohm)
- Admittance Y (siemens)
- Active power P (watt)
- Reactive power Q (var)
- Apparent power S (VA)

### Electrical laws

- Kirchhoff’s current law
- Kirchhoff’s voltage law
- Ohm's law
- Impedances, admittances in series and parallel
- Voltage divider and current divider
- Millman's theorem
- Joule's first law (S=I²Z)
- Power law (S=V.I*)

### Others features

- Bode plot (with cursors and sliders)
- User-defined transfer function H(jω)
- Digital filter frequency response

### AC Circuit diagram 

Circuit should only contain : 
   
- independent sine voltage source  
- independent sine current source    
- resistors, inductors, capacitors

#### Example circuit  

```
                  VL
           <---------------------
                          L1
            +------+    _  _  _
      --->--| R1   |---/ \/ \/ \-----+-------+
        IL  +------+                 |       |
                                     |       |
    ^                             IR v       v IC
    |                                |       |      ^
    |                              +---+     |  C1  |
    |                              |   |   -----    |
Vin |                              |R2 |   -----    | Vout
    |                              |   |     |      |
    |                              +---+     |      |
    |                                |       | 
                                     |       |
      -------------------------------+-------+

```

Datas :  
Vin = 5 Vrms  
Inductor : L1 = 100 mH ; R1 = 180 Ω  
R2 = 2.2 kΩ ; C1 = 330 nF     

What are the IL, IR, IC currents ?  
What are the VL, Vout voltages ?  
What is the frequency response Vout/Vin ?


```python  
>>> from acelectricity import *
>>> Vin = Voltage(5)  # Vrms
>>> Zr1 = Impedance(r=180)
>>> Zl1 = Impedance(l=0.1)
>>> Zr2 = Impedance(r=2200)
>>> Zc1 = Impedance(c=330e-9)

>>> Zeq1 = 1/(1/Zr2 + 1/Zc1)  # impedances in parallel
>>> # or Zeq1 = Zr2//Zc1
>>> Zeq1
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
>>> Zeq = Zr1 + Zl1 + Zeq1  # impedances in series
>>> Zeq(2000)  # @ 2000 Hz
(206.11818300356995+1018.3560443060462j)
>>> IL = Vin/Zeq  # Ohm's law
>>> IL.properties(2000)
Frequency (Hz) : 2000
Angular frequency (rad/s) : 12566.4

Complex current : 0.000954663-0.00471665j
Amplitude (Arms) : 0.00481229
Amplitude (A) : 0.00680561
Amplitude (dBA ref 1 Arms) : -46.3529621108357
Phase (degrees) : -78.5577
Phase (radians) : -1.37109
i(t) = 0.00680561×sin(12566.4×t -1.371091)

>>> Vout = IL*Zeq1  # Ohm's law
>>> VL = Vin-Vout  # Kirchhoff’s voltage law
>>> IC = Vout/Zc1  # Ohm's law
>>> IR = IL-IC  # Kirchhoff’s current law
>>> H = Vout/Vin  # transfer function

>>> # draw Bode plot and save datas
>>> H.bode(title='Vout/Vin transfer function', filename='h.csv')
>>> IL.bode(magnitude_unit='default', yscale='linear', title='IL current')
>>> Zeq.bode(yscale='log', title='Zeq frequency response')
>>> Zeq.bode_imag(title='Zeq reactance frequency response')
>>> show()
```

![screenshot1](https://framagit.org/fsincere/ac-electricity/uploads/2a805bf67525bb8962d543e0674adfcd/image1.png)

Zoom and data cursors :  

![screenshot1b](https://framagit.org/fsincere/ac-electricity/uploads/1be007c117d04613104a05372843f813/image1b.png)

![screenshot2](https://framagit.org/fsincere/ac-electricity/uploads/c63c67fa0d68621b730cce1901beada3/image2.png)

![screenshot2b](https://framagit.org/fsincere/ac-electricity/uploads/80acf919527ea3b74a3c89ced4fa62e9/image2b.png)

![screenshot2b1](https://framagit.org/fsincere/ac-electricity/uploads/49e6093bb979273c3b464cdbb0f79939/image2b1.png)

#### Impedances and admittances

```python
>>> Yr2 = 1/Zr2
>>> Yc1 = 1/Zc1
>>> Yc1
Complex admittance (S) : 0+0.00207345j @ 1.0 kHz
>>> 1/Yc1
Complex impedance (Ω) : 0-482.288j @ 1.0 kHz
>>> 1/(Yr2+Yc1)
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
>>> Zr2*(Zc1/(Zr2+Zc1))
Complex impedance (Ω) : 100.88-460.173j @ 1.0 kHz
```

#### Law class

```python
>>> law = Law()
>>> # voltage divider
>>> Vout = law.VoltageDivider(vtotal=Vin, z=Zr2//Zc1, z2=Zr1+Zl1)
>>> Vout
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> Vin*(Zeq1/Zeq)
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> # Millman's theorem
>>> gnd = Voltage(0)
>>> Vout = law.Millman(v_z=[(Vin, Zr1+Zl1), (gnd, Zr2), (gnd, Zc1)])
>>> Vout
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> (Vin/(Zr1+Zl1))/(1/(Zr1+Zl1) +1/Zr2 +1/Zc1)
Complex voltage (Vrms) : -2.28808-6.8219j @ 1.0 kHz
>>> Vout/Vin
Ratio : -0.457615-1.36438j @ 1.0 kHz
>>> # current divider
>>> IC = law.CurrentDivider(itotal=IL, z=Zc1, z2=Zr2)
>>> IC
Complex current (Arms) : 0.0141449-0.00474421j @ 1.0 kHz
>>> IL*Zr2/(Zr2 +Zc1)
Complex current (Arms) : 0.0141449-0.00474421j @ 1.0 kHz
```

#### Electrical power, Joule's first law

```python
>>> S = IL*Vin  # input source complex power
>>> S.properties(1000)
Frequency (Hz) : 1000
Angular frequency (rad/s) : 6283.19

Complex power : 0.0655242+0.0392254j

Active power P (W) : +0.0655242
Reactive power Q (var) : +0.0392254
Apparent power S (VA) : 0.0763678

Phase (degrees) : +30.9064
Phase (radians) : +0.539419
Power factor PF : 0.8580073402000852

Active power (dBW ref 1 W) : -11.835985322667693

>>> Sr1 = law.Joule(z=Zr1, i=IL)
>>> Sr1
Complex power (W): 0.0419907+0j @ 1.0 kHz
>>> Zr1*IL*IL
Complex power (W): 0.0419907+0j @ 1.0 kHz
>>> Sr2 = law.Joule(z=Zr2, v=Vout)
>>> Sr2
Complex power (W): 0.0235334 @ 1.0 kHz
>>> Sl1 = Zl1*IL*IL
Complex power (W): 0+0.146575j @ 1.0 kHz
>>> Sc1 = Zc1*IC*IC
Complex power (W): 0-0.10735j @ 1.0 kHz
>>> Sr1 +Sr2 +Sc1 +Sl1
Complex power (W): 0.0655242+0.0392254j @ 1.0 kHz
```

#### Parameters analysis

```python  
>>> Vin.RMS = 10
>>> Vin.phase = 45
>>> Zr1.r = 100
>>> Zl1.l = 0.22
>>> Zr2.r = 1000
>>> Zc1.c = 100e-9
>>> H.bode(title='Vout/Vin transfer function', filename='h2.csv')
>>> IL.bode(magnitude_unit='default', yscale='linear', title='IL current')
>>> show()
```

![screenshot2c](https://framagit.org/fsincere/ac-electricity/uploads/6f8870f523174dcd475945ee43a0b19f/image2c.png)

![screenshot2d](https://framagit.org/fsincere/ac-electricity/uploads/cf3c70fe19e3b3b80434ed9d10d7741d/image2d.png)


```python  
>>> for Zr2.r in [10, 100, 1e3, 1e4]:
        H.bode(title="Vout/Vin with R2={} Ω".format(Zr2.r))
>>> show()
```

#### Add matplotlib widgets : slider and button   

```python
>>> fig, ax1, ax2, mag, ph = H.bode(title='Vout/Vin transfer function')
>>> fig.subplots_adjust(left=0.15, bottom=0.35, right=0.85, top=0.9)

>>> ax_r1 = plt.axes([0.15, 0.20, 0.4, 0.03])
>>> ax_l1 = plt.axes([0.15, 0.15, 0.4, 0.03])
>>> ax_r2 = plt.axes([0.15, 0.10, 0.4, 0.03])
>>> ax_c1 = plt.axes([0.15, 0.05, 0.4, 0.03])

>>> slider_r1 = Slider(ax_r1, 'r1 (Ω)', 10, 300,
    valinit=Zr1.r, valstep=1)
>>> slider_l1 = Slider(ax_l1, 'l1 (H)', 0.01, 1,
    valinit=Zl1.l, valstep=0.01)
>>> slider_r2 = Slider(ax_r2, 'r2 (Ω)', 1e3, 1e4,
    valinit=Zr2.r, valstep=10)
>>> slider_c1 = Slider(ax_c1, 'c1 (nF)', 100, 1000,
    valinit=Zc1.c*1e9, valstep=1)

>>> def update(val):
        Zr1.r = slider_r1.val
        Zl1.l = slider_l1.val
        Zr2.r = slider_r2.val
        Zc1.c = slider_c1.val*1e-9
        xvalues = mag.get_xdata()
        # H.db() method, according to H.bode() parameters :
        # magnitude_unit='db' (default)
        # help(H) for more information
        magnitudes = [H.db(x) for x in xvalues]
        # H.phase_deg() method, according to H.bode() parameters :
        # phase_unit='degrees' (default)
        phases = [H.phase_deg(x) for x in xvalues]
        mag.set_ydata(magnitudes)
        ph.set_ydata(phases)

>>> slider_r1.on_changed(update)
>>> slider_l1.on_changed(update)
>>> slider_r2.on_changed(update)
>>> slider_c1.on_changed(update)

>>> ax_button = plt.axes([0.7, 0.10, 0.15, 0.06])
>>> button = Button(ax_button, 'Autoscale')

>>> def autoscale(event):
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

>>> button.on_clicked(autoscale)
>>> show()
```

![screenshot2e](https://framagit.org/fsincere/ac-electricity/uploads/c857708a7d3b6cbe3d90eb584148dc04/image2e.png)

### User-defined transfer function

#### Example 1 : second order band-pass filter

```python
>>> from acelectricity import *
>>> # static gain, damping value, normal angular frequency
>>> a, z, wn = 10, 0.1, 1000*2*math.pi
>>> H = Ratio(fw=lambda w: a*(2*z*1j*w/wn)/(1+2*z*1j*w/wn-(w/wn)**2))
>>> H.bode(filename='H.csv')
>>> a, z, wn = 100, 0.5, 10000
>>> H.bode(filename='H2.csv')
>>> show()
```

or :  

```python
>>> a, z, wn = 10, 0.1, 1000*2*math.pi
>>> H = Ratio.transfer_function(numerator=[0, a*(2*z*1j/wn)],
    denominator=[1, 2*z*1j/wn, -1/wn**2])
>>> H.bode(filename='H3.csv')
>>> a, z, wn = 100, 0.5, 10000
>>> # new instance
>>> H = Ratio.transfer_function(numerator=[0, a*(2*z*1j/wn)],
    denominator=[1, 2*z*1j/wn, -1/wn**2])
>>> H.bode(filename='H4.csv')
>>> show()
```

#### Example 2 : cascaded series, parallel filters

```python
>>> from acelectricity import *
>>> # first order low-pass filter
>>> wn = 10000
>>> Hlp = Ratio(fw=lambda w: 1/(1+1j*w/wn))
>>> # first order high-pass filter
>>> Hhp = Ratio(fw=lambda w: 1/(1+1j*wn/w))
>>> Hs = Hlp*Hhp  # cascaded series filters
>>> Hs.bode()
>>> Hp = Hlp+Hhp  # parallel filters
>>> Hp.bode()
>>> show()
```

#### Example 3 : linear control system

```
          +      +------+
     -->---(X)---| G(w) |----+--->--
          - |    +------+    |
            |                |
            |    +------+    |
            +----| H(w) |-<--+
                 +------+

```

```python
>>> from acelectricity import *
>>> # feedforward transfer function
>>> # first order low-pass filter
>>> wn = 10000
>>> G = Ratio.transfer_function([1], [1, 1j/wn])
>>> # feedback transfer function
>>> H = Ratio.transfer_function([10])  # constant
>>> # open-loop transfer function
>>> Hopenloop = G*H
>>> Hopenloop.bode()
>>> # closed-loop transfer function
>>> Hcloseloop = G/(1+Hopenloop)
>>> Hcloseloop.bode()
>>> show()
```

### Digital filter frequency response

```
y(n) = 0.1x(n) +1.6y(n-1) -0.7y(n-2)
```

```python
>>> from acelectricity import *
>>> fs = 100000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[0.1], a=[1, -1.6, 0.7])
>>> H.bode(xmin=0, xmax=fs/2, xscale='linear',
    title='IIR digital filter')
>>> show()
```

![screenshot3](https://framagit.org/fsincere/ac-electricity//uploads/187f9f3c728601a54f688b08817224a7/image3.png)

```
y(n) = (x(n)+x(n-1)+...+x(n-7))/8
```

```python
>>> from acelectricity import *
>>> fs = 10000  # sampling rate (Hz)
>>> H = Ratio.digital_filter(fs=fs, b=[1/8]*8)
>>> H.bode(xmin=0, xmax=fs/2, xscale='linear',
    magnitude_unit='default', title='FIR digital filter')
>>> show()
```

![screenshot4](https://framagit.org/fsincere/ac-electricity/uploads/7c9d44218cdc34d91c58e661959190eb/image4.png)


### Custom default frequency

```python
>>> from acelectricity import *
>>> Yc = Admittance(c=220e-6)
>>> Yc
Complex admittance (S) : 0+1.3823j @ 1.0 kHz
>>> ElectricalQuantity.DEFAULT_FREQUENCY = 50
>>> Yc
Complex admittance (S) : 0+0.069115j @ 50 Hz
>>> 1/Yc
Complex impedance (Ω) : 0-14.4686j @ 50 Hz
```

### Goodies

#### Ideal filters

```python
>>> from acelectricity import *
>>> def lp(w):
        wn = 10000
        return 1 if w < wn else 0.001
>>> def hp(w):
        wn = 1000
        return 10 if w > wn else 0.001
>>> def bp(w):
        wn1, wn2 = 1000, 10000
        return 1 if wn2 > w > wn1 else 0.001
>>> def notch(w):
        wn1, wn2 = 4000, 5000
        return 0.001 if wn2 > w > wn1 else 1
>>> def allpass(w):
        wn = 10000
        return 1j if w > wn else -1j
>>> Hlp = Ratio(fw=lp)
>>> Hhp = Ratio(fw=hp)
>>> Hbp = Ratio(fw=bp)
>>> Hnotch = Ratio(fw=notch)
>>> Hallpass = Ratio(fw=allpass)
>>> Hallpass.bode(title='Ideal all-pass filter')
>>> (Hhp+Hlp).bode(title='Ideal filter Bode plot')
>>> show()
```

![screenshot5](https://framagit.org/fsincere/ac-electricity/uploads/049f8ba9a1f11e08b6d2fcbb3be8d700/image5.png)

![screenshot6](https://framagit.org/fsincere/ac-electricity/uploads/f0fcb4b3039df6774abfa8c885b9f04f/image6.png)

Note : remember that ideal filters are not realizable (not causal).  

#### Asymptotic Bode diagram

```python
>>> def lp1(w):
        # first order low-pass filter 1/(1+1j*w/wn)
        # asymptotic approximation
        wn = 1000
        return 1 if w < wn else 1/(1j*w/wn)
>>> def lp2(w):
        wn = 30000
        return 1 if w < wn else 1/(1j*w/wn)
>>> Hlp1 = Ratio(fw=lp1);Hlp2 = Ratio(fw=lp2)
>>> (Hlp1*Hlp2).bode(title='Asymptotic Bode plot')
>>> show()
```

![screenshot7](https://framagit.org/fsincere/ac-electricity/uploads/fcd30dd740138e241330522c24a05071/image7.png)

### Advantages and limitations

This module manages basic arithmetic operations ```+ - * /``` as well as ```//``` which designates two impedances in parallel.  

The dimensional homogeneity is checked :  

```python
>>> V3 = V1 - V2 + I3  # V+A -> Error
TypeError : Voltage expected
>>> I1 = Current(2)
>>> I = I1 + 0.5  # A+number -> Error
TypeError : Current expected
>>> I2 = Current(0.5, phase=30)
>>> I = I1 + I2
>>> I
Complex current (Arms) : 2.43301+0.25j @ 1.0 kHz
>>> I = 5*I2 - V1/Z1 + I3
```

The result of any operation must give a quantity whose unit is one of : V, A, Ω, S, W (or ratio).  
Otherwise, you will get an error :   

```python
>>> Z1/V1  # Ω/V -> 1/A -> Error
TypeError
>>> U2*(Z3/(Z2+Z3))  # V*(Ω/Ω) -> V*() -> V
>>> U2*Z3/(Z2+Z3)  # V*Ω -> Error
TypeError
>>> S = V1*(V1/Z1)  # V*(V/Ω) -> V*A -> W
>>> S = V1*V1/Z1    # V*V -> Error
TypeError
```

### See also  

[https://pypi.org/project/dc-electricity](https://pypi.org/project/dc-electricity)
