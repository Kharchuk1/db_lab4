INSERT INTO student (outid, birth, sextype_id, location_id,
                    areaname, tername, regtypename, tertypename, 
                    profile, language,
                    eoname, eotypename, eoregname, eoareaname,
                    eotername, eoparent)
SELECT zno.outid, zno.birth, sex_type.id, location.id,
       zno.areaname, zno.tername, zno.regtypename, zno.tertypename,
       zno.classprofilename, zno.classlangname, 
       zno.eoname, zno.eotypename, zno.eoregname, zno.eoareaname,
       zno.eotername, zno.eoparent
FROM zno
INNER JOIN sex_type ON sex_type.name = zno.sextypename
INNER JOIN location ON location.name = zno.regname;