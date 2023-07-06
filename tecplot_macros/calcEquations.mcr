#!MC 1410
$!AlterData 
  Equation = '{x}={r}*sin({th})*cos({ph})'
$!AlterData 
  Equation = '{y}={r}*sin({th})*sin({ph})'
$!AlterData 
  Equation = '{z}={r}*cos({th})'
$!AlterData 
  Equation = '{vx}=sin({th})*cos({ph})*{vr}+cos({th})*cos({ph})*{vclt}-sin({ph})*{vlon}'
$!AlterData 
  Equation = '{vy}=sin({th})*sin({ph})*{vr}+cos({th})*sin({ph})*{vclt}+cos({ph})*{vlon}'
$!AlterData 
  Equation = '{vz}=cos({th})*{vr}-sin({th})*{vclt}'
$!AlterData 
  Equation = '{bx}=sin({th})*cos({ph})*{Br}+cos({th})*cos({ph})*{Bclt}-sin({ph})*{Blon}'
$!AlterData 
  Equation = '{by}=sin({th})*sin({ph})*{Br}+cos({th})*sin({ph})*{Bclt}+cos({ph})*{Blon}'
$!AlterData 
  Equation = '{bz}=cos({th})*{Br}-sin({th})*{Bclt}'
$!AlterData 
  Equation = '{b}=sqrt({bx}*{bx}+{by}*{by}+{bz}*{bz})'
$!AlterData 
  Equation = '{jx}=ddy({bz})-ddz({by})'
$!AlterData 
  Equation = '{jy}=ddz({bx})-ddx({bz})'
$!AlterData 
  Equation = '{jz}=ddx({by})-ddy({bx})'
$!AlterData 
  Equation = '{j}=sqrt({jx}*{jx}+{jy}*{jy}+{jz}*{jz})'
$!AlterData 
  Equation = '{divV}=ddx({vx})+ddy({vy})+ddz({vz})'
$!AlterData 
  Equation = '{T}={P}/({n}*1.38*10**-17)'
$!AlterData 
  Equation = '{bz_over_by}={bz}/{by}'
$!ThreeDAxis XDetail{VarNum = 13}
$!ThreeDAxis YDetail{VarNum = 14}
$!ThreeDAxis ZDetail{VarNum = 15}