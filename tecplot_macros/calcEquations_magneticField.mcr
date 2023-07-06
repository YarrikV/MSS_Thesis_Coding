#!MC 1410
$!AlterData 
  Equation = '{bx}=sin({th})*cos({ph})*{Br}+cos({th})*cos({ph})*{Bclt}-sin({ph})*{Blon}'
$!AlterData 
  Equation = '{by}=sin({th})*sin({ph})*{Br}+cos({th})*sin({ph})*{Bclt}+cos({ph})*{Blon}'
$!AlterData 
  Equation = '{bz}=cos({th})*{Br}-sin({th})*{Bclt}'
$!AlterData 
  Equation = '{b}=sqrt({bx}*{bx}+{by}*{by}+{bz}*{bz})'