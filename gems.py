import discord
import random as r
import time as t
import DB
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

message_crime = ["You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal ",
"tu as volé une pomme qui vaut ", "tu as gangé le loto ! prends tes ", "j'ai plus d'idée prends ça: "]
# 4 phrases
message_gamble = ["tu as remporté le pari ! tu obtiens ","Une grande victoire pour toi ! tu gagnes ",
"bravo prends ", "heu.... "]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
class Item:

	def __init__(self,nom,achat,vente,poid,idmoji):
		self.nom = nom
		self.achat = achat
		self.vente = vente
		self.poid = poid
		self.idmoji = idmoji

objet = [Item("pickaxe",20,5,5,608748195291594792),Item("iron_pickaxe",150,60,10,608748194775433256),Item("fishingrod",15,5,3,608748194318385173),Item("cobblestone",3,1,0.5,608748492181078131)
,Item("iron",30,r.randint(9,11),1,608748195685597235),Item("gold",100,r.randint(45, 56),1,608748194754723863),Item("ruby",150,r.randint(74, 82),1,608748194406465557),Item("diamond",200,r.randint(98, 120),1,608748194750529548)
,Item("fish",5,2,0.5,608762539605753868),Item("tropical_fish",60,r.randint(25, 36),1,608762539030872079)]

#anti-spam
couldown_xl = 10
couldown_l = 6 # l pour long
couldown_c = 4 # c pour court
couldown_sc = 2 # sc pour super court
# nb de sec nécessaire entre 2 commandes

def spam(ID,couldown):
	time = DB.valueAt(ID, "com_time")
	# on récupère le la date de la dernière commande
	return(time < t.time()-couldown)


def nom_ID(nom):
	if len(nom) == 21 :
		ID = int(nom[2:20])
	elif len(nom) == 22 :
		ID = int(nom[3:21])
	else :
		print("mauvais nom")
		ID = "prout"
	return(ID)

def addGems(ID, nbGems):
	"""
	Permet d'ajouter un nombre de gems à quelqu'un. Il nous faut son ID et le nombre de gems.
	Si vous souhaitez en retirer mettez un nombre négatif.
	Si il n'y a pas assez d'argent sur le compte la fonction retourne un nombre
	strictement inférieur à 0.
	"""
	old_value = DB.valueAt(ID, "gems")
	new_value = int(old_value) + nbGems
	if new_value >= 0:
		DB.updateField(ID, "gems", new_value)
		print("Le compte de "+str(ID)+ " est maintenant de: "+str(new_value))
	else:
		print("Il n'y a pas assez sur ce compte !")
	return str(new_value)



def nbElements(ID, nameElem):
	"""
	Permet de savoir combien il y'a de nameElem dans l'inventaire de ID
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nameElem in inventory:
		return inventory[nameElem]
	else:
		return 0



def get_idmogi(nameElem):
	"""
	Permet de connaitre l'idmoji de l'item
	"""
	test = False
	for c in objet:
		if c.nom == nameElem:
			test = True
			return c.idmoji
	if test == False:
		return 0



def addInv(ID, nameElem, nbElem):
	"""
	Permet de modifier le nombre de nameElem pour ID
	Pour en retirer mettez nbElemn en négatif
	"""
	inventory = DB.valueAt(ID, "inventory")
	if nbElements(ID, nameElem) > 0 and nbElem < 0:
		inventory[nameElem] += nbElem
	elif nbElem >= 0:
		if nbElements(ID, nameElem) == 0:
			inventory[nameElem] = nbElem
		else :
			inventory[nameElem] += nbElem
	else:
		print("On ne peut pas travailler des élements qu'il n'y a pas !")
		return 404
	DB.updateField(ID, "inventory", inventory)

#===============================================================

class Gems(commands.Cog):

	def __init__(self,ctx):
		return(None)



	@commands.command(pass_context=True)
	async def begin(self, ctx):
		"""pour initialiser la base de donnée !"""
		ID = ctx.author.id
		await ctx.channel.send(DB.newPlayer(ID))



	@commands.command(pass_context=True)
	async def crime(self, ctx):
		"""commets un crime et gagne des gems !"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			gain = r.randint(5,10)
			msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
			addGems(ID, gain)
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"

		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def bal(self, ctx, nom = None):
		"""êtes vous riche ou pauvre ? bal vous le dit """
		ID = ctx.author.id
		if spam(ID,couldown_sc):
			#print(nom)
			if nom != None:
				ID = nom_ID(nom)
				gem = DB.valueAt(ID, "gems")
				msg = nom+" a actuellement : "+str(gem)+" :gem: !"
			else:
				gem = DB.valueAt(ID, "gems")
				msg = "tu as actuellement : "+str(gem)+" :gem: !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_sc)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def gamble(self, ctx,valeur):
		"""| gamble [valeur] | avez vous l'ame d'un parieur ?  """
		valeur = int(valeur)
		ID = ctx.author.id
		if spam(ID,couldown_xl):
			if r.randint(0,3) == 0:
				gain = valeur*3
				# l'espérence est de 0 sur la gamble
				msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
				addGems(ID, gain)
			else:
				val = 0-valeur
				addGems(ID,val)
				msg = "Dommage tu as perdu "+str(valeur)+":gem:"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_xl)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def buy (self, ctx,item,nb = 1):
		"""permet d'acheter les items vendus au marché"""
		ID = ctx.author.id
		if spam(ID,couldown_c):
			test = True
			nb = int(nb)
			for c in objet :
				if item == c.nom :
					test = False
					prix = 0 - (c.achat*nb)
					if addGems(ID, prix) >= "0":
						addInv(ID, c.nom, nb)
						msg = "Vous venez d'acquérir {0} <:gem_{1}:{2}>`{1}` !".format(nb, c.nom, c.idmoji)
					else :
						msg = "Désolé, nous ne pouvons pas executer cet achat, vous n'avez pas assez d'argent en banque"
					break
			if test :
				msg = "Cet item n'est pas vendu au marché !"
		else :
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def mine(self, ctx):
		""" minez compagnons !! vous pouvez récuperer 1 à 5 bloc de cobblestones, 1 lingot de fer, 1 lingot d'or ou 1 diamant brut"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			#print(nbElements(ID, "pickaxe"))
			nbrand = r.randint(0,99)
			#----------------- Pioche en fer -----------------
			if nbElements(ID, "iron_pickaxe") >= 1:
				if r.randint(0,49)==0:
					addInv(ID,"iron_pickaxe", -1)
					msg = "pas de chance tu as cassé ta <:gem_iron_pickaxe:{}>`pioche en fer` !".format(get_idmogi("iron_pickaxe"))
				else :
					if nbrand > 20 and nbrand < 50:
						addInv(ID, "iron", 1)
						msg = "tu as obtenue 1 <:gem_iron:{}>`lingot de fer` !".format(get_idmogi("iron"))
					elif nbrand > 5 and nbrand < 20:
						addInv(ID, "gold", 1)
						msg = "tu as obtenue 1 <:gem_gold:{}>`lingot d'or` !".format(get_idmogi("gold"))
					elif nbrand < 5:
						addInv(ID, "diamond", 1)
						msg = "tu as obtenue 1 <:gem_diamond:{}>`diamant brut` !".format(get_idmogi("diamond"))
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "tu as obtenue un bloc de <:gem_cobblestone:{}>`cobblestone` !".format(get_idmogi("cobblestone"))
						else :
							msg = "tu as obtenue {} blocs de <:gem_cobblestone:{}>`cobblestone` !".format(nbcobble, get_idmogi("cobblestone"))

			#----------------- Pioche normal -----------------
			elif nbElements(ID, "pickaxe") >= 1:
				if r.randint(0,29)==0:
					addInv(ID,"pickaxe", -1)
					msg = "pas de chance tu as cassé ta <:gem_pickaxe:{}>`pioche` !".format(get_idmogi("pickaxe"))
				else :
					if nbrand < 20:
						addInv(ID, "iron", 1)
						msg = "tu as obtenue 1 <:gem_iron:{}>`lingot de fer` !".format(get_idmogi("iron"))
					else:
						nbcobble = r.randint(1,5)
						addInv(ID, "cobblestone", nbcobble)
						if nbcobble == 1 :
							msg = "tu as obtenue 1 bloc de <:gem_cobblestone:{}>`cobblestone` !".format(get_idmogi("cobblestone"))
						else :
							msg = "tu as obtenue {} blocs de <:gem_cobblestone:{}>`cobblestone` !".format(nbcobble, get_idmogi("cobblestone"))
			else:
				msg = "il faut acheter ou forger une pioche !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def fish(self, ctx):
		""" Pechons compagnons !! vous pouvez récuperer 1 à 5 :fish: ou 1 :tropical_fish:"""
		ID = ctx.author.id
		if spam(ID,couldown_l):
			nbrand = r.randint(0,99)
			#print(nbElements(ID, "fishingrod"))
			if nbElements(ID, "fishingrod") >= 1:
				if r.randint(0,39)==0:
					addInv(ID,"fishingrod," -1)
					msg = "pas de chance tu as cassé ta <:gem_fishingrod:{}>`canne à peche` !".format(get_idmogi("fishingrod"))
				else :
					if nbrand < 20:
						addInv(ID, "tropical_fish", 1)
						msg = "tu as obtenue 1 <:gem_tropical_fish:{}>`tropical_fish` !".format(get_idmogi("tropical_fish"))
					elif nbrand > 20 and nbrand < 80:
						nbfish = r.randint(1,5)
						addInv(ID, "fish", nbfish)
						msg = "tu as obtenue {} <:gem_fish:{}>`fish` !".format(nbfish, get_idmogi("fish"))
					else:
						msg = "Pas de poisson pour toi aujourd'hui :cry: "
			else:
				msg = "il te faut une <:gem_fishingrod:{}>`canne à peche` pour pecher, tu en trouvera une au marché !".format(get_idmogi("fishingrod"))
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_l)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def forge(self, ctx, item, nb = 1):
		""" Forgons une pioche en fer: Pour cela tu aura besoin de 4 lingots de fer et d'1 :pick:pickaxe"""
		ID = ctx.author.id
		if spam(ID,couldown_c):
			if item == "iron_pickaxe":
				#print("iron: {}, pickaxe: {}".format(nbElements(ID, "iron"), nbElements(ID, "pickaxe")))
				nb = int(nb)
				nbIron = 4*nb
				nbPickaxe = 1*nb
				if nbElements(ID, "iron") >= nbIron and nbElements(ID, "pickaxe") >= nbPickaxe:
					addInv(ID, "iron_pickaxe", nb)
					addInv(ID, "pickaxe", -nbPickaxe)
					addInv(ID, "iron", -nbIron)
					msg = "Bravo, tu as réussi à forger {0} :iron_pickaxe: !".format(nb)
				elif nbElements(ID, "iron") < nbIron and nbElements(ID, "pickaxe") < nbPickaxe:
					msg = "tu n'as pas assez de lingot d'iron et de pioche pour forger {0} :iron_pickaxe: !".format(nb)
				elif nbElements(ID, "iron") < nbIron:
					nbmissing = (nbElements(ID, "iron") - nbIron)*-1
					msg = "Il te manque {0} lingots de fer pour forger {1} :iron_pickaxe: !".format(nbmissing, nb)
				else:
					nbmissing = (nbElements(ID, "pickaxe") - nbPickaxe)*-1
					msg = "Il te manque {0} :pick:pickaxe pour forger {1} :iron_pickaxe: !".format(nbmissing, nb)
			else:
				msg = "Impossible d'exécuter le craft de cette item !"
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def inv (self, ctx):
		"""permet de voir ce que vous avez dans le ventre !"""
		ID = ctx.author.id
		member = ctx.author
		inv = DB.valueAt(ID, "inventory")
		msg_inv = " "
		#print (inv)
		#msg="**ton inventaire**\n"
		for c in objet:
			for x in inv:
				if c.nom == str(x):
					if inv[x] > 0:
						msg_inv = msg_inv+"<:gem_{0}:{2}>`{0}`: `{1}`\n".format(str(x), str(inv[x]), c.idmoji)

		msg = discord.Embed(title = "Ton inventaire",color= 6466585, description = msg_inv)
		#msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
		await ctx.channel.send(embed = msg)



	@commands.command(pass_context=True)
	async def market (self, ctx):
		"""permet de voir tout les objets que l'on peux acheter ou vendre !"""
		ID = ctx.author.id
		if spam(ID,couldown_sc):
			d_market="Permet de voir tout les objets que l'on peux acheter ou vendre !\n\n"
			for c in objet :
				d_market += "<:gem_{0}:{4}>`{0}`: Vente **{1}**, Achat **{2}**, Poid **{3}**\n".format(c.nom,c.vente,c.achat,c.poid,c.idmoji)
			msg = discord.Embed(title = "Le marché",color= 2461129, description = d_market)

			DB.updateComTime(ID)
			await ctx.channel.send(embed = msg)
		else:
			msg = "il faut attendre "+str(couldown_sc)+" secondes entre chaque commande !"
			await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def sell (self, ctx,item,nb = 1):
		"""| sell [item] [nombre] |Les valeurs d'échange :cobblestone => 1 iron => 10"""
		#cobble 1, iron 10, gold 50, diams 100
		ID = ctx.author.id
		if spam(ID,couldown_c):
			nb = int(nb)
			if nbElements(ID, item) >= nb:
				addInv(ID, item, -nb)
				test = True
				for c in objet:
					if item == c.nom:
						test = False
						gain = c.vente*nb
						addGems(ID, gain)
						msg ="tu as vendu {0} <:gem_{1}:{3}>`{1}` pour {2} :gem: !".format(nb,item,gain,c.idmoji)
						break
				if test:
					msg = "cette objet n'existe pas"
			else:
				#print("Pas assez d'élement")
				msg = "Vous n'avez pas assez de "+str(item)+". Il vous en reste : "+ str(nbElements(ID, item))
			DB.updateComTime(ID)
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)



	@commands.command(pass_context=True)
	async def pay (self, ctx, nom, gain):
		"""| pay [nom] [gain] | donner de l'argent à vos amis ! """
		ID = ctx.author.id
		if spam(ID,couldown_c):
			try:
				gain = int(gain)
				don = -gain
				ID_recu = nom_ID(nom)
				if int(DB.valueAt(ID, "gems")) >= 0:
					print(ID_recu)
					addGems(ID_recu, gain)
					addGems(ID,don)
					msg = "<@{0}> donne {1}:gem: à <@{2}> !".format(ID,gain,ID_recu)
				else:
					msg = "<@{0}> n'a pas assez pour donner à <@{2}> !".format(ID,gain,ID_recu)
				DB.updateComTime(ID)
			except ValueError:
				msg = "la commande est mal formulée"
				pass
		else:
			msg = "il faut attendre "+str(couldown_c)+" secondes entre chaque commande !"
		await ctx.channel.send(msg)

def setup(bot):
	bot.add_cog(Gems(bot))
	open("fichier_txt/cogs.txt","a").write("Gems\n")
