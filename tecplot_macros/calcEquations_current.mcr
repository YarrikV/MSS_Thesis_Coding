#!MC 1410
$!AlterData 
  Equation = '{jx}=ddy({bz})-ddz({by})'
$!AlterData 
  Equation = '{jy}=ddz({bx})-ddx({bz})'
$!AlterData 
  Equation = '{jz}=ddx({by})-ddy({bx})'
$!AlterData 
  Equation = '{j}=sqrt({jx}*{jx}+{jy}*{jy}+{jz}*{jz})'