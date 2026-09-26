
			function convertDate(){
				x = document.getElementById('id_StartDate').value
				y = parseInt(x.substr(0, 4))
				m = parseInt(x.substr(5, 2))
				d = parseInt(x.substr(8, 2))
				function jalaliToUTCTimeStamp(year, month, day) {
                const format = new Intl.DateTimeFormat('en-u-ca-persian', {
                dateStyle: 'short',
                timeZone: "UTC"
                });
                let g = new Date(Date.UTC(2000, month, day));
                g = new Date(g.setUTCDate(g.getUTCDate() + 226867));
                const gY = g.getUTCFullYear(g) - 2000 + year;
                g = new Date(((gY < 0) ? "-" : "+") + ("00000" + Math.abs(gY)).slice(-6) + "-" + ("0" + (g.getUTCMonth(g) + 1)).slice(-2) + "-" + ("0" + (g.getUTCDate(g))).slice(-2));
                let [pM, pD, pY] = [...format.format(g).split("/")], i = 0;
                g = new Date(g.setUTCDate(g.getUTCDate() + ~~(year * 365.25 + month * 30.44 + day - (pY.split(" ")[0] * 365.25 + pM * 30.44 + pD * 1)) - 2));
                while (i < 4) {
                [pM, pD, pY] = [...format.format(g).split("/")];
                if (pD == day && pM == month && pY.split(" ")[0] == year) return g;
                g = new Date(g.setUTCDate(g.getUTCDate() + 1));
                i++;
                }
            throw new Error('Invalid Persian Date!');
            }
        z = jalaliToUTCTimeStamp(y, m, d)
        z= z.toISOString().split('T')[0]
	    document.getElementById('id_StartDate').value = z
        console.log(z)
			}

			function convertDateadmin(){
				x = document.getElementById('id_start_date').value
				y = parseInt(x.substr(0, 4))
				m = parseInt(x.substr(5, 2))
				d = parseInt(x.substr(8, 2))
                e = document.getElementById('id_end_date').value
				ye = parseInt(e.substr(0, 4))
				me = parseInt(e.substr(5, 2))
				de = parseInt(e.substr(8, 2))
				function jalaliToUTCTimeStamp(year, month, day) {
                const format = new Intl.DateTimeFormat('en-u-ca-persian', {
                dateStyle: 'short',
                timeZone: "UTC"
                });
                let g = new Date(Date.UTC(2000, month, day));
                g = new Date(g.setUTCDate(g.getUTCDate() + 226867));
                const gY = g.getUTCFullYear(g) - 2000 + year;
                g = new Date(((gY < 0) ? "-" : "+") + ("00000" + Math.abs(gY)).slice(-6) + "-" + ("0" + (g.getUTCMonth(g) + 1)).slice(-2) + "-" + ("0" + (g.getUTCDate(g))).slice(-2));
                let [pM, pD, pY] = [...format.format(g).split("/")], i = 0;
                g = new Date(g.setUTCDate(g.getUTCDate() + ~~(year * 365.25 + month * 30.44 + day - (pY.split(" ")[0] * 365.25 + pM * 30.44 + pD * 1)) - 2));
                while (i < 4) {
                [pM, pD, pY] = [...format.format(g).split("/")];
                if (pD == day && pM == month && pY.split(" ")[0] == year) return g;
                g = new Date(g.setUTCDate(g.getUTCDate() + 1));
                i++;
                }
            throw new Error('Invalid Persian Date!');
            }
        if (x !== ''){
            z = jalaliToUTCTimeStamp(y, m, d)
            z= z.toISOString().split('T')[0]
            document.getElementById('id_start_date').value = z
        }
        if (e !== ''){
            ze = jalaliToUTCTimeStamp(ye, me, de)
            ze= ze.toISOString().split('T')[0]
	        document.getElementById('id_end_date').value = ze
        }
        
			}