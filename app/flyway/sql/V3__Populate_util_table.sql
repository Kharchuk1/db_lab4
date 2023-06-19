INSERT INTO location(name) 
SELECT DISTINCT ukrptregname FROM public.zno
WHERE ukrptregname IS NOT NULL AND ukrptareaname IS NOT NULL AND ukrpttername IS NOT NULL;

INSERT INTO sex_type(name) 
SELECT DISTINCT sextypename FROM public.zno;

INSERT INTO test_status(name) 
SELECT DISTINCT ukrteststatus FROM public.zno
WHERE ukrteststatus IS NOT NULL;