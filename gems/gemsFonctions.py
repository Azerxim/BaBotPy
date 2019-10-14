import discord
import random as r
import time as t
import datetime as dt
from DB import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from operator import itemgetter

message_crime = ["Vous avez volé la Société Eltamar et vous êtes retrouvé dans un lac, mais vous avez quand même réussi à voler" #You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal
,"Tu as volé une pomme qui vaut"
,"Tu as volé une carotte ! Prend tes"
, "Tu voles un bonbon ! Prend tes"
, "Tu as gangé au loto ! Prends tes"
, "J'ai plus d'idée prends ça:"]
# 4 phrases
message_gamble = ["Tu as remporté le pari ! Tu obtiens"
,"Une grande victoire pour toi ! Tu gagnes"
,"Bravo prends"
, "Heu...."
,"Pourquoi jouer à Fortnite quand tu peux gamble! Prends tes"]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité

# Taille max de l'Inventaire
invMax = 10000

global globalvar
globalvar = -1

def incrementebourse():
	global globalvar
	if globalvar == 0:
		loadItem()
		globalvar += 1
		print("\nGems >> Mise à jour de la bourse")
	elif globalvar >= 120:
		globalvar = 0
	else:
		globalvar += 1



def itemBourse(item, type):
	if type == "vente":
		if item == "iron":
			Prix = r.randint(9,11)
		elif item == "gold":
			Prix = r.randint(45, 56)
		elif item == "diamond":
			Prix = r.randint(98, 120)
		elif item == "emerald":
			Prix = r.randint(148, 175)
		elif item == "ruby":
			Prix = r.randint(1800, 2500)
		elif item == "tropicalfish":
			Prix = r.randint(25, 36)
		elif item == "blowfish":
			Prix = r.randint(25, 36)
		elif item == "octopus":
			Prix = r.randint(40,65)
		elif item == "grapes":
			Prix = r.randint(10,20)
		else:
			Prix = 404
		return Prix

	elif type == "achat":
		if item == "grapes":
			Prix = r.randint(20,30)
		elif item == "planting_plan":
			Prix = r.randint(900, 1150)
		else:
			Prix = 404
		return Prix



def loadItem():
	class Item:

		def __init__(self,nom,vente,achat,poids,idmoji,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.idmoji = idmoji
			self.type = type

	global objetItem
	objetItem = [Item("cobblestone", 1, 3, 4, 608748492181078131, "minerai")
	,Item("iron", itemBourse("iron", "vente"), 30, 10, 608748195685597235, "minerai")
	,Item("gold", itemBourse("gold", "vente"), 100, 20, 608748194754723863, "minerai")
	,Item("diamond", itemBourse("diamond", "vente"), 200, 40, 608748194750529548, "minerai")
	,Item("emerald", itemBourse("emerald", "vente"), 320, 50, 608748194653798431, "minerai")
	,Item("ruby", itemBourse("ruby", "vente"), 3000, 70, 608748194406465557, "minerai")
	,Item("fish", 2, 5, 2, 608762539605753868, "poisson")
	,Item("tropicalfish", itemBourse("tropicalfish", "vente"), 60, 8, 608762539030872079, "poisson")
	,Item("blowfish", itemBourse("blowfish", "vente"), 60, 8, 618058831863218176, "poisson")
	,Item("octopus", itemBourse("octopus", "vente"), 90, 16, 618058832790421504, "poisson")
	,Item("seed", 1, 2, 0.5, 618058917930336266, "plante")
	,Item("oak", 400, 500, 50, 625698779076755485, "plante")
	,Item("spruce", 600, 800, 70, 625698795744657409, "plante")
	,Item("palm", 850, 1200, 60, 625698810773110785, "plante")
	,Item("wheat", 1100, 2000, 3, 625701009586520064, "plante")
	,Item("cookie", 30, 40, 1, "", "consommable")
	,Item("grapes", itemBourse("grapes", "vente"), itemBourse("grapes", "achat"), 1, "", "consommable")
	,Item("wine_glass", 120, 210, 2, "", "consommable")
	,Item("pumpkin", 50, 125, 5, 633219431107133450, "halloween")
	,Item("pumpkinpie", 1000, 1200, 5, 633261963467685888, "halloween")
	,Item("candy", 1, 2, 1, "", "halloween")
	,Item("lollipop", 5, 12, 2, "", "halloween")
	,Item("backpack", 1, 5000, -200, 616205834451550208, "special")
	,Item("fishhook", 50, 225, 1, 633207161241075743, "special")]


	class Outil:

		def __init__(self,nom,vente,achat,poids,durabilite,idmoji,type):
			self.nom = nom
			self.vente = vente
			self.achat = achat
			self.poids = poids
			self.durabilite = durabilite
			self.idmoji = idmoji
			self.type = type

	global objetOutil
	objetOutil = [Outil("pickaxe", 5, 20, 15, 75, 625702466360574004, "")
	,Outil("iron_pickaxe", 80, 300, 70, 250, 608748194775433256, "forge")
	,Outil("diamond_pickaxe", 500, 1800, 150, 600, 625702527135907851, "forge")
	,Outil("fishingrod", 5, 15, 25, 150, 608748194318385173, "")
	,Outil("sword", 50, 200, 55, 100, 625702555200258058, "forge")
	,Outil("planting_plan", 100, itemBourse("planting_plan", "achat"), 3, 3, 631038633398501376, "")
	,Outil("bank_upgrade", 0, 10000, 10000, None ,421465024201097237, "bank")]


##############################################
class Box:

	def __init__(self,nom, titre, achat , min, max):
		self.nom = nom
		self.titre = titre
		self.achat = achat
		self.min = min
		self.max = max

objetBox = [Box("commongems", "Gems Common", 300, 100, 500)
,Box("raregems", "Gems Rare", 3000, 1000, 5000)
,Box("legendarygems", "Gems Legendary", 30000, 10000, 50000)]



class Recette:

	def __init__(self,nom,type, nb1,item1, nb2,item2, nb3,item3, nb4,item4):
		self.nom = nom
		self.type = type
		self.nb1 = nb1
		self.item1 = item1
		self.nb2 = nb2
		self.item2 = item2
		self.nb3 = nb3
		self.item3 = item3
		self.nb4 = nb4
		self.item4 = item4

objetRecette = [Recette("iron_pickaxe", "forge", 10, "iron", 1, "pickaxe", 0, "", 0, "")
,Recette("diamond_pickaxe", "forge", 25, "diamond", 1, "iron_pickaxe", 0, "", 0, "")
,Recette("sword", "forge", 6, "iron", 1, "oak", 0, "", 0, "")]



class Trophy:

	def __init__(self,nom,desc,type,mingem):
		self.nom = nom
		self.desc = desc
		self.type = type
		self.mingem = mingem #nombre de gems minimum necessaire

objetTrophy = [Trophy("Gamble Jackpot", "`Gagner plus de 10000`:gem:` au gamble`", "special", 10000)
,Trophy("Super Jackpot :seven::seven::seven:", "`Gagner le super jackpot sur la machine à sous`", "special", 0)
,Trophy("Mineur de Merveilles", "`Trouvez un `<:gem_ruby:608748194406465557>`ruby`", "special", 0)
,Trophy("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`", "special", 0)
,Trophy("Gems 500", "`Avoir 500`:gem:", "unique", 500)
,Trophy("Gems 1k", "`Avoir 1k`:gem:", "unique", 1000)
,Trophy("Gems 5k", "`Avoir 5k`:gem:", "unique", 5000)
,Trophy("Gems 50k", "`Avoir 50k`:gem:", "unique", 50000)
,Trophy("Gems 200k", "`Avoir 200k`:gem:", "unique", 200000)
,Trophy("Gems 500k", "`Avoir 500k`:gem:", "unique", 500000)
,Trophy("Gems 1M", "`Avoir 1 Million`:gem:", "unique", 1000000)
,Trophy("Gems 10M", "`Avoir 10 Millions`:gem:", "unique", 10000000)
,Trophy("Gems 100M", "`Avoir 100 Millions`:gem:", "unique", 100000000)
,Trophy("Gems 500M", "`Avoir 500 Millions`:gem:", "unique", 500000000)
,Trophy("Le Milliard !!!", "`Avoir 1 Milliard`:gem:", "unique", 1000000000)]



class StatGems:

	def __init__(self,nom,desc):
		self.nom = nom
		self.desc = desc

objetStat = [StatGems("DiscordCop Arrestation", "`Nombre d'arrestation par la DiscordCop`")
,StatGems("DiscordCop Amende", "`Nombre d'ammende recue par la DiscordCop`")
,StatGems("Gamble Win", "`Nombre de gamble gagné`")
,StatGems("Super Jackpot :seven::seven::seven:", "`Nombre de super jackpot gagné sur la machine à sous`")
,StatGems("Mineur de Merveilles", "`Nombre de `<:gem_ruby:608748194406465557>`ruby` trouvé")
,StatGems("La Squelatitude", "`Avoir 2`:beer:` sur la machine à sous`")]

#anti-DB.spam
couldown_12h = 86400/2 # 12h
couldown_8h = 86400/3 # 8h
couldown_6h = 86400/4 # 6h
couldown_4h = 86400/6 # 4h
couldown_3h = 86400/8 # 3h
couldown_2h = 86400/12 # 2h
couldown_1h = 86400/24 # 1h
couldown_30 = 86400/48 # 30 min
couldown_xxxl = 30
couldown_xxl = 15
couldown_xl = 10
couldown_l = 8 # l pour long
couldown_c = 6 # c pour court
# nb de sec nécessaire entre 2 commandes


def get_idmoji(nameElem):
	"""
	Permet de connaitre l'idmoji de l'item
	"""
	test = False
	for c in objetItem:
		if c.nom == nameElem:
			test = True
			return c.idmoji

	for c in objetOutil:
		if c.nom == nameElem:
			test = True
			return c.idmoji
	if test == False:
		return 0



def get_price(nameElem, type = None):
	"""
	Permet de connaitre le prix de l'item
	"""
	test = False
	if type == None or type == "vente":
		for c in objetItem:
			if c.nom == nameElem:
				test = True
				return c.vente

		for c in objetOutil:
			if c.nom == nameElem:
				test = True
				return c.vente
	elif type == "achat":
		for c in objetItem:
			if c.nom == nameElem:
				test = True
				return c.achat

		for c in objetOutil:
			if c.nom == nameElem:
				test = True
				return c.achat
	if test == False:
		return 0



def testInvTaille(ID):
	inv = DB.valueAt(ID, "inventory")
	tailletot = 0
	for c in objetOutil:
		for x in inv:
			if c.nom == str(x):
				if inv[x] > 0:
					tailletot += c.poids*int(inv[x])

	for c in objetItem:
		for x in inv:
			if c.nom == str(x):
				if inv[x] > 0:
					tailletot += c.poids*int(inv[x])

	if tailletot <= invMax:
		return True
	else:
		return False



def testTrophy(ID, nameElem):
	"""
	Permet de modifier le nombre de nameElem pour ID dans les trophées
	Pour en retirer mettez nbElemn en négatif
	"""
	trophy = DB.valueAt(ID, "trophy")
	gems = DB.valueAt(ID, "gems")
	i = 2
	for c in objetTrophy:
		nbGemsNecessaire = c.mingem
		if c.type == "unique":
			if nameElem in trophy:
				i = 0
			elif gems >= nbGemsNecessaire:
				i = 1
				DB.add(ID, "trophy", c.nom, 1)
	return i



def addDurabilite(ID, nameElem, nbElem):
	"""
	Modifie la durabilité de l'outil nameElem
	"""
	durabilite = DB.valueAt(ID, "durabilite")
	if DB.nbElements(ID, "inventory", nameElem) > 0 and nbElem < 0:
		durabilite[nameElem] += nbElem
	elif nbElem >= 0:
		durabilite[nameElem] = nbElem
	else:
		# print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "durabilite", durabilite)



def get_durabilite(ID, nameElem):
	"""
	Permet de savoir la durabilite de nameElem dans l'inventaire de ID
	"""
	nb = DB.nbElements(ID, "inventory", nameElem)
	if nb > 0:
		durabilite = DB.valueAt(ID, "durabilite")
		for c in objetOutil:
			if nameElem == c.nom:
				if nameElem in durabilite:
					return durabilite[nameElem]
	else:
		return -1



def recette(ctx):
	"""Liste de toutes les recettes disponibles !"""
	d_recette="Permet de voir la liste de toutes les recettes disponible !\n\n"
	d_recette+="▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Forge**\n"
	for c in objetOutil:
		for r in objetRecette :
			if c.type == "forge":
				if c.nom == r.nom:
					d_recette += "<:gem_{0}:{1}>`{0}`: ".format(c.nom,c.idmoji)
					if r.nb1 > 0:
						d_recette += "{0} <:gem_{1}:{2}>`{1}` ".format(r.nb1, r.item1, get_idmoji(r.item1))
					if r.nb2 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb2, r.item2, get_idmoji(r.item2))
					if r.nb3 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb3, r.item3, get_idmoji(r.item3))
					if r.nb4 > 0:
						d_recette += "et {0} <:gem_{1}:{2}>`{1}` ".format(r.nb4, r.item4, get_idmoji(r.item4))
					d_recette += "\n"

	msg = discord.Embed(title = "Recettes",color= 15778560, description = d_recette)
	return msg



def taxe(solde, pourcentage):
	soldeTaxe = solde * pourcentage
	soldeNew = solde - soldeTaxe
	taxe = (soldeTaxe, soldeNew)
	return taxe


class GemsTest(commands.Cog):

	def __init__(self,ctx):
		return(None)


	@commands.command(pass_context=True)
	async def gemstest(self, ctx):
		await ctx.channel.send(":regional_indicator_t::regional_indicator_e::regional_indicator_s::regional_indicator_t:")



def setup(bot):
	bot.add_cog(GemsTest(bot))
