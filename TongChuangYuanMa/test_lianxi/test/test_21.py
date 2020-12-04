import re
import requests
import time
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont
from PIL import ImageGrab


# str = """
#     <TTGlyph name="uniF487" xMin="0" yMin="-40" xMax="394" yMax="715">
#       <contour>
#         <pt x="393" y="-40" on="1"/>
#         <pt x="292" y="-19" on="1"/>
#         <pt x="305" y="563" on="1"/>
#         <pt x="274" y="503" on="0"/>
#         <pt x="206" y="486" on="1"/>
#         <pt x="161" y="454" on="0"/>
#         <pt x="116" y="453" on="1"/>
#         <pt x="99" y="519" on="1"/>
#         <pt x="186" y="574" on="0"/>
#         <pt x="244" y="604" on="1"/>
#         <pt x="271" y="649" on="0"/>
#         <pt x="305" y="662" on="1"/>
#         <pt x="312" y="694" on="0"/>
#         <pt x="324" y="710" on="1"/>
#         <pt x="382" y="714" on="1"/>
#         <pt x="386" y="-26" on="1"/>
#       </contour>
#       <instructions/>
#     </TTGlyph>
#     """
# str2 = """
# <TTGlyph name="uniF5DC" xMin="0" yMin="-27" xMax="391" yMax="711">
#       <contour>
#         <pt x="382" y="-26" on="1"/>
#         <pt x="292" y="-26" on="1"/>
#         <pt x="292" y="546" on="1"/>
#         <pt x="259" y="507" on="0"/>
#         <pt x="200" y="486" on="1"/>
#         <pt x="153" y="462" on="0"/>
#         <pt x="127" y="446" on="1"/>
#         <pt x="104" y="532" on="1"/>
#         <pt x="174" y="563" on="0"/>
#         <pt x="249" y="615" on="1"/>
#         <pt x="258" y="637" on="0"/>
#         <pt x="296" y="649" on="1"/>
#         <pt x="312" y="673" on="0"/>
#         <pt x="311" y="710" on="1"/>
#         <pt x="390" y="697" on="1"/>
#         <pt x="382" y="-19" on="1"/>
#       </contour>
#       <instructions/>
#     </TTGlyph>
#     """
str3 = """
<TTGlyph name="uniF617" xMin="0" yMin="-36" xMax="525" yMax="711">
      <contour>
        <pt x="43" y="335" on="1"/>
        <pt x="43" y="463" on="0"/>
        <pt x="69" y="544" on="1"/>
        <pt x="95" y="637" on="0"/>
        <pt x="148" y="667" on="1"/>
        <pt x="201" y="710" on="0"/>
        <pt x="271" y="710" on="1"/>
        <pt x="398" y="710" on="0"/>
        <pt x="459" y="617" on="1"/>
        <pt x="487" y="574" on="0"/>
        <pt x="504" y="508" on="1"/>
        <pt x="524" y="447" on="0"/>
        <pt x="520" y="335" on="1"/>
        <pt x="520" y="284" on="0"/>
        <pt x="514" y="228" on="1"/>
        <pt x="508" y="166" on="0"/>
        <pt x="494" y="126" on="1"/>
        <pt x="466" y="46" on="0"/>
        <pt x="414" y="4" on="1"/>
        <pt x="362" y="-24" on="0"/>
        <pt x="282" y="-35" on="1"/>
        <pt x="176" y="-34" on="0"/>
        <pt x="108" y="37" on="1"/>
        <pt x="43" y="127" on="0"/>
      </contour>
      <contour>
        <pt x="131" y="335" on="1"/>
        <pt x="135" y="158" on="0"/>
        <pt x="177" y="95" on="1"/>
        <pt x="218" y="35" on="0"/>
        <pt x="282" y="35" on="1"/>
        <pt x="343" y="39" on="0"/>
        <pt x="385" y="96" on="1"/>
        <pt x="425" y="155" on="0"/>
        <pt x="428" y="335" on="1"/>
        <pt x="438" y="515" on="0"/>
        <pt x="378" y="576" on="1"/>
        <pt x="344" y="635" on="0"/>
        <pt x="218" y="635" on="0"/>
        <pt x="181" y="583" on="1"/>
        <pt x="135" y="515" on="0"/>
        <pt x="135" y="332" on="1"/>
      </contour>
      <instructions/>
    </TTGlyph>

    """

x = [int(i) for i in re.findall(r'<pt x="(.*?)" y=', str3)]
y = [int(i) for i in re.findall(r'y="(.*?)" on=', str3)]
print(x)
print(y)
plt.plot(x, y)
plt.savefig(r"F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/34.png")
plt.show()


  
