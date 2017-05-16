from numpy import vstack
from flask import Flask, flash,redirect,render_template, request
import sys,time,csv
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from scipy.cluster.vq import kmeans,vq,whiten
import pygal,json
from collections import defaultdict
import time


application = Flask(__name__)
global result,k


@application.route("/", methods=["GET"])
def main():
         return render_template('index.html')

@application.route('/clustering',methods=['POST'])
def cluster():
	start = time.time()
    testfile =request.files['file']
    k = request.form['cluster']
	col1 = request.form['col1']
	col2 = request.form['col2']
    csv_data = csv.reader(file(testfile.filename))
	csv_data.next()
        vector = []
        for line in csv_data:
		if(line[int(col1)]==''):
			x=0
		elif(line[int(col2)]==''):
			y=0
		else:
			x =line[int(col1)]
			y =line[int(col2)]
                vector_element = []
                vector_element.append(float(x))
                vector_element.append(float(y))
                vector.append(vector_element)

        data = vstack(vector)
        centroids, distortion = kmeans(data,int(k))
        idx,_ = vq(data,centroids)
        total_points =[]
	global result
        result=defaultdict(list)
        for i in range(int(k)):

                column_1 = data[idx==i, 0]
		column_2 = data[idx==i, 1]

                count = 0
                for name in column_1:
                	count +=1
		
		for j in range(int(count)):
			print column_1[j],column_2[j],i+1
			res=[]
			res.append(column_1[j])
			res.append(column_2[j])
			x=i+1
			#res.append(i+1)
			#result[x].append(res)
		#print result	
                print "Cluster: " + str(i+1) + "   Total cluster points: " +str(count)
                total_points.append(count)
                centroid_points = []
                for row in centroids:
                	cent = []
                        cent.append(row[0])
                        cent.append(row[1])
                        centroid_points.append(cent)
			x=i+1
			result[x].append(cent)
                print(centroid_points[0:])
		stop = time.time()
		stime = stop-start
		print stime
        return render_template('output.html',result =result)

		
@application.route('/visualization',methods=['POST'])
def render():
	try:
		xy_chart = pygal.XY(stroke=False)
		xy_chart.title = 'Clustering'
		for i,j in result.iteritems():
			xy_chart.add("%s" %i, [y for y in j])
			xy_chart.add("%s" %i, [y for y in j])
			
		graph_data=xy_chart.render_data_uri()
		return render_template("graphing.html",graph_data=graph_data)
	except Exception, e:
                return(str(e))
				
		xy_chart = pygal.XY(stroke=False)
		xy_chart.title = 'Clustering'
		xy_chart.add()
		xy_chart.add("%s" %i, [y for y in j])

		chart = pygal.Bar(stroke=False)
		chart.add('Cluster2', [{'value': 7, 'label': 'This is the first'}])
		chart.add('Cluster1', [{'value': 11, 'label': 'This is the second'}])
		chart.add('Cluster3', [{'value' : 11, 'label':'This is third'}])
		graph_data = chart.render_data_uri()
		return render_template("graphing.html",graph_data=graph_data)
        except Exception, e:
                return(str(e))



if __name__=='__main__':
        application.run(host=' ')



