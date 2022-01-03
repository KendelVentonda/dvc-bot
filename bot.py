import discord
import random
import re
from discord.ext import commands

bot = commands.Bot(command_prefix='$', description='DvC Wuerfel Bot')

def wurf(wuerfel: int):
	wuerfe = []
	erfolg = 0
	sechs = 0
	for i in range(wuerfel):
		x = (random.randint(1,6))
		wuerfe.append(x)
		if x > 3:
			erfolg += 1
		if x == 6:
			sechs += 1
	return wuerfe , erfolg , sechs
	wuerfel = 0
	wuerfe.clear()

@bot.event
async def on_ready():
    print('Angemeldet als ')
    print(bot.user.name)


@bot.command(description="$r X - Du kannst X durch eine Anzahl an sechsseitigen Würfeln ersetzen und ich würfel für dich die Erfolge.", pass_context=True)
async def r(ctx, a: int):
	_wuerfe , _erfolg , _sechs = wurf(a)
	await bot.say(str(_wuerfe) + " Sechsen: " + str(_sechs) + " Erfolge: " + str(_erfolg))
	_wuerfe.clear()
	while _sechs > 0:
		__wuerfe , __erfolg , __sechs = wurf(_sechs)
		await bot.say(str(__wuerfe) + " Sechsen: " + str(__sechs) + " Erfolge: " + str(__erfolg))
		__wuerfe.clear()
		_sechs = __sechs
		__sechs = 0
		_erfolg += __erfolg
	if _erfolg == 0:
		await bot.say("Wow, {} hatte einen fatalen Fehlschlag! :scream: Was kannst du eigentlich?".format(ctx.message.author.mention))
	else:
		await bot.say("{} hatte **".format(ctx.message.author.mention) + str(_erfolg) + "** Erfolge")

@bot.command(description="Hiermit würfel ich für dich einen Prozentwurf.")
async def pro():
	prozent = (random.randint(1,100))
	await bot.say("Chance liegt bei " + str(prozent) + "%.")

# CHECK der FERTIGKEITEN und ATTRIBUTE

@bot.command(description="$c X - Du kannst X durch den Wert deiner Probe eingeben und ich würfel dir die Erfolge.")
async def c(eingabe: str):
	erstes = 0
	zweites = 0

	searchObj = re.search(r'([0-9][0-9][0-9]|[0-9][0-9]|[0-9]).([0-9][0-9][0-9]|[0-9][0-9]|[0-9])', eingabe, re.X)
	erstes = int(searchObj.group(1))
	zweites = int(searchObj.group(2))

	cwuerfe = []
	cerfolg = 0
	csechs = 0
	for i in range(erstes):
		cx = (random.randint(1,zweites))
		cwuerfe.append(cx)

	await bot.say("Geworfen wurden " + str(erstes) + " mal " + str(zweites) + " und ergaben " + str(cwuerfe))

# WETTER

@bot.command(description="Du möchtest wissen welches Wetter wir derzeit im Spiel haben?")
async def wetter():

	weigensch = ["sonnig", "windig", "leicht regnerisch", "stark regnerisch", "kalt", "bewölkt", "bedeckt aber trocken", "gewittrig"]
	wzufall = (random.randint(0,7))

	await bot.say("Es ist " + str(weigensch[wzufall]) + ".")


# PHYSISCHER ANGRIFF

@bot.command(description="Wähle einen Gegner aus (am besten über @) und gebe den Wert deines physischen Angriffs als Zahl ein. Der Bot würfelt für dich. Der getaggte Gegner muss dann seinen physischen Verteidigungswert angeben. Ein eventueller Schaden wird berechnet. Liegt dieser bei 8 und mehr, erhält der Gegner eine private Nachricht über die schwere Verletzung.", pass_context=True)
async def bam(ctx, op: discord.Member, a: int):
	__wuerfe , __erfolg , __sechs = wurf(a)
	__wuerfe.clear()
	while __sechs > 0:
		___wuerfe , ___erfolg , ___sechs = wurf(__sechs)
		___wuerfe.clear()
		__sechs = ___sechs
		___sechs = 0
		__erfolg += ___erfolg
	if __erfolg == 0:
		await bot.say("{} schlug voll daneben!".format(ctx.message.author.mention))
	else:
		await bot.say("{} griff ".format(ctx.message.author.mention) + str(op.mention) + " mit **" + str(__erfolg) + "** Erfolgen an! " + str(op.nick) + " gib bitte deinen Wert für physische Verteidigung ein.")
		antwort = await bot.wait_for_message(author = op, timeout=90)
		antwortVer = antwort.content
		verteidigung = int(antwortVer)

		wuerfeVer , erfolgVer , sechsVer = wurf(verteidigung)
		wuerfeVer.clear()
		while sechsVer > 0:
			wuerfeVer2 , erfolgVer2 , sechsVer2 = wurf(sechsVer)
			wuerfeVer2.clear()
			sechsVer = sechsVer2
			sechsVer2 = 0
			erfolgVer += erfolgVer2

		difangriff = int(__erfolg) - int(erfolgVer)
		if 0 < difangriff < 8:
			await bot.say(str(op.mention) + " verteidigt mit " + str(erfolgVer) + " und nimmt " + str(difangriff) + " TP Schaden!")
		elif difangriff >= 8:
			verletzung = (random.randint(0,100))
			if 0 <= verletzung <= 10:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du hast dir deinen rechten Arm verletzt und deine Angriffe erhalten einen Malus von -3. Fertigkeiten, für die du deinen rechten Arm benötigst einen Malus von -2.")
			elif 11 <= verletzung <= 20:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du hast dir deinen linken Arm verletzt und deine Angriffe erhalten einen Malus von -3. Fertigkeiten, für die du deinen linken Arm benötigst einen Malus von -2.")
			elif 21 <= verletzung <= 40:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Dein Bein schmerzt. Deine Geschwindigkeit ist reduziert und alle Fertigkeiten, die dein Bein benötigen, erhalten einen Malus von -2.")
			elif 41 <= verletzung <= 55:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du hast innere Verletzungen und jede hastige Bewegung führt zu einem TP-Verlust.")
			elif 56 <= verletzung <= 64:
				ohnmacht = (random.randint(1,4))
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du wurdest am Kopf verletzt und bist für " + str(ohnmacht) + " Stunden bewusstlos. Deine Wahrnehmung ist um -2 Punkte gemindert.")
			elif 65 <= verletzung <= 69:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du hast eine Verletzung am Hals. Jede hastige Bewegung hat eine 10 prozentige Möglichkeit zum Tod zu führen.")
			elif 70 <= verletzung <= 85:
				laehmung = (random.randint(1,4))
				laehmung2 = (random.randint(1,10))
				if laehmung2 == 1:
					if laehmung == 1:
						await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Deine Wirbelsäule ist verwundet und dein linker Arm dauerhaft gelähmt.")
					if laehmung == 2:
						await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Deine Wirbelsäule ist verwundet und dein rechter Arm dauerhaft gelähmt.")
					if laehmung == 3:
						await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Deine Wirbelsäule ist verwundet und dein linkes Bein dauerhaft gelähmt.")
					if laehmung == 4:
						await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Deine Wirbelsäule ist verwundet und dein rechtes Bein dauerhaft gelähmt.")
				else:
					await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Deine Wirbelsäule ist verwundet.")
			elif 86 <= verletzung <= 91:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du blutest im Gesicht. Diese Verletzung senkt dein Charisma um -2.")
			elif 92 <= verletzung <= 96:
				blindheit = (random.randint(1,6))
				if blindheit == 1:
					await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du wurdest an beiden Augen verletzt und bist vollständig blind.")
				else:
					await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du wurdest am Auge verwundet. An einem Auge wirst du blind.")
			elif 97 <= verletzung <= 100:
				taubheit = (random.randint(1,6))
				if taubheit == 1:
					await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du wurdest an beiden Ohren verwundet und bist vollständig taub.")
				else:
					await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Du wurdest am Ohr verwundet. An einem Ohr wirst du taub.")
			else:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verletzt. Das sollte sich ein Arzt ansehen.")
			await bot.say(str(op.mention) + " verteidigt mit " + str(erfolgVer) + ", nimmt " + str(difangriff) + " TP Schaden und wird schwer verletzt!")
		else:
			await bot.say(str(op.mention) + " blockierte {}'s Angriff gekonnt!".format(ctx.message.author.mention))


# MAGISCHER ANGRIFF

@bot.command(description="Wähle einen Gegner aus (am besten über @) und gebe den Wert deines magischen Angriffs als Zahl ein. Der Bot würfelt für dich. Der getaggte Gegner muss dann seinen magischen Verteidigungswert angeben. Ein eventueller Schaden wird berechnet. Liegt dieser bei 8 und mehr, erhält der Gegner eine private Nachricht über die schwere Verletzung.", pass_context=True)
async def zap(ctx, op: discord.Member, a: int):
	__wuerfe , __erfolg , __sechs = wurf(a)
	__wuerfe.clear()
	while __sechs > 0:
		___wuerfe , ___erfolg , ___sechs = wurf(__sechs)
		___wuerfe.clear()
		__sechs = ___sechs
		___sechs = 0
		__erfolg += ___erfolg
	if __erfolg == 0:
		await bot.say("{} verlor die Verbindung zur Æther!".format(ctx.message.author.mention))
	else:
		await bot.say("{} griff ".format(ctx.message.author.mention) + str(op.mention) + " mit **" + str(__erfolg) + "** Erfolgen an! " + str(op.nick) + " gib bitte deinen Wert für magische Verteidigung ein.")
		antwort = await bot.wait_for_message(author = op, timeout=90)
		antwortVer3 = antwort.content
		verteidigung3 = int(antwortVer3)

		wuerfeVer3 , erfolgVer3 , sechsVer3 = wurf(verteidigung3)
		wuerfeVer3.clear()
		while sechsVer3 > 0:
			wuerfeVer4 , erfolgVer4 , sechsVer4 = wurf(sechsVer3)
			wuerfeVer4.clear()
			sechsVer3 = sechsVer4
			sechsVer4 = 0
			erfolgVer3 += erfolgVer4

		difangriff3 = int(__erfolg) - int(erfolgVer3)
		if 0 < difangriff3 < 8:
			await bot.say(str(op.mention) + " wehrt mit " + str(erfolgVer3) + "ab und nimmt " + str(difangriff3) + " TP Schaden!")
		elif difangriff3 >= 8:
			verletzung = (random.randint(0,100))
			if 0 <= verletzung <= 10:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du hast eine organische psychische Störung und benötigst immer 6 Erfolge auf Weisheit um dich an etwas zu erinnern.")
			elif 11 <= verletzung <= 20:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du wirst innerhalb der nächsten 2 Wochen rauschmittelabhängig.")
			elif 21 <= verletzung <= 40:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Es entwickelt sich eine Wahnvorstellung, weshalb du mit imaginären Personen interagierst.")
			elif 41 <= verletzung <= 55:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du bekommst eine Depression, weshalb deine Initiative auf 0 sinkt.")
			elif 56 <= verletzung <= 64:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du entwickelst eine Belastungsstörung. Eine Phobie quält dich. Sobald du ihr begegnest musst du 4 Erfolge auf Wille bekommen um sie zu überstehen.")
			elif 65 <= verletzung <= 69:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Eine Verhaltensauffälligkeit gesellt sich hinzu. Welche genau ist im Grundregelwerk nachzulesen.")
			elif 70 <= verletzung <= 85:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du hast eine Persönlichkeitsstörung. Welche genau ist im Grundregelwerk nachzulesen.")
			elif 86 <= verletzung <= 91:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Deine Intelligenz wird gemindert. Dein Attribut Weisheit und damit verbundene Fertigkeiten können nicht mehr aufgewertet werden.")
			elif 92 <= verletzung <= 96:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Du leidest an einer Entwicklungsstörung, wodurch Manipulation und Charisma einen Malus von -3 erhalten.")
			elif 97 <= verletzung <= 100:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. Dich belastet eine emotionale Störung. Deine emotionale Bindung zu anderen ist gemindert und du wirst ausgesprochen pragmatisch.")
			else:
				await bot.send_message(op, "Du wurdest mit " + str(verletzung) + "% schwer verwundet. ")
			await bot.say(str(op.mention) + " wehrt mit " + str(erfolgVer3) + " ab, nimmt " + str(difangriff3) + " TP Schaden und wird schwer verwundet!")
		else:
			await bot.say(str(op.mention) + " zeigte gegenüber {} einen eisernen Willen!".format(ctx.message.author.mention))

# HANDEL-BOT

@bot.command(pass_context=True)
async def handel(ctx):
	await bot.say('Du möchtest einkaufen. Suchst du Waffen, Rüstung, Essenzen oder sonstiges?')
	response = await bot.wait_for_message(author = ctx.message.author, timeout=30)
	if response.clean_content.lower() == 'waffen':
		await bot.say('Du willst Waffen.')
	elif response.clean_content.lower() == 'rüstung':
		await bot.say('Du willst Rüstung.')
	elif response.clean_content.lower() == 'essenzen':
		await bot.say('Du willst Essenzen.')
	elif response.clean_content.lower() == 'sonstiges':
		await bot.say('Du willst sonstiges.')
	else:
		await bot.say("That isn't a valid response.")


#@bot.command(pass_context=True)
#async def name(ctx):
#    await bot.say("{} is your name".format(ctx.message.author.mention))


bot.run('NDU0MzkxNzgxODUzNzU3NDQw.DfyPRg.kzOSLWCwSbxHbCea_bvq1Swiksg')
