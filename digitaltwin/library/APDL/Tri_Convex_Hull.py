# This is convex hull algorithm for identifying contact between parts for Ansys APDL analysis.
# Needs testing and tuning.



# import sys
# sys.path.append('E:/1Sheffield/Project/Projects/DDI/Back_End')
# import Service_Layer.Connectoro as a
# import numpy as np
# from decimal import Decimal
# import math

# class convexHull:

#     def __init__(self) -> None:
#         pass
    
#     def main(self, cvxHull, chkPts):
#         value = self.vectors(cvxHull, chkPts)
#         return(value)
   
# #______________________FIRST SORT IT____________________________Then check why we have 666 points
#     def vectors(self, cvxHull, chkPts):
#         j = 0

#           # looping through covex Hull
#         while j < len(cvxHull):
#             u0 = np.array([])  #vectors 1 and 2 of the Hull for 1st vertex
#             v0 = np.array([])
#             u1 = np.array([])  #vectors 1 and 2 of the Hull for 2nd vertex
#             v1 = np.array([])
            
#             #Vectors for first vertex [j][0]    
#             u0 = np.append(u0, cvxHull[j][0]-cvxHull[j][3]) # x co-ordinate
#             u0 = np.append(u0, cvxHull[j][1]-cvxHull[j][4]) # y
#             v0 = np.append(v0, cvxHull[j][0]-cvxHull[j][6])
#             v0 = np.append(v0, cvxHull[j][1]-cvxHull[j][7])
            
#             #Vectors for second vertex [j][1]
#             u1 = np.append(u1, cvxHull[j][3]-cvxHull[j][0]) 
#             u1 = np.append(u1, cvxHull[j][4]-cvxHull[j][1]) 
#             v1 = np.append(v1, cvxHull[j][3]-cvxHull[j][6])
#             v1 = np.append(v1, cvxHull[j][4]-cvxHull[j][7])
            
#             #_________________________ANGLE of u1 v1______________________________________________________________
#             # formula for angle between vectors. i.e, cos angle = dot product/ product of magnitude of two vectors
#             # Decimal to avoid error of float and decimal and to get more accurate values
#             uv0 = (u0[0]*v0[0])+(u0[1]*v0[1])
#             if uv0 == 0:
#                 angDeg0 = 90
#             else :
#                 moduv0 = Decimal(math.sqrt(u0[0]**2 + u0[1]**2))*Decimal(math.sqrt(v0[0]**2+v0[1]**2))
#                 if uv0/moduv0 < 0:
#                     if ((uv0/moduv0)*(-1)) > 1 :
#                         angRd0 =  math.acos(1)
#                     else:
#                         angRd0 = math.pi - (math.acos((uv0/moduv0)*(-1)))
#                 elif uv0/moduv0 > 1:
#                     angRd0 =  math.acos(1) 
#                 else:
#                     angRd0 = math.acos(uv0/moduv0)
#                 angDeg0 = (angRd0 *(180/(math.pi)))

#             #_________________________ANGLE of u2 v2______________________________________________________________ 
#             uv1 = (u1[0]*v1[0])+(u1[1]*v1[1])
#             if uv1 == 0:
#                 angDeg1 = 90
#             else:
#                 moduv1 = Decimal(math.sqrt(u1[0]**2 + u1[1]**2))*Decimal(math.sqrt(v1[0]**2+v1[1]**2))
#                 if uv1/moduv1 < 0:
#                     if ((uv1/moduv1)*(-1)) > 1 :
#                         angRd1 =  math.acos(1)
#                     else:
#                         angRd1 = (math.pi)-(math.acos((uv1/moduv1)*(-1)))
#                 elif uv1/moduv1 > 1:
#                     angRd1 =  math.acos(1)   
#                 else : 
#                     angRd1 = (math.acos(uv1/moduv1))
#                 angDeg1 = (angRd1 *(180/(math.pi)))
            
#             Hullangl = np.array([angDeg0,angDeg1])
            
#             #Range of points to shorlist from prt c/s
#             xmin = min(cvxHull[j][0], cvxHull[j][3], cvxHull[j][6])
#             xmax = max(cvxHull[j][0], cvxHull[j][3], cvxHull[j][6])
#             ymin = min(cvxHull[j][1], cvxHull[j][4], cvxHull[j][7])
#             ymax = max(cvxHull[j][1], cvxHull[j][4], cvxHull[j][7])
#             range = np.array([xmin, xmax, ymin, ymax])            
#             shtLstPts = self.shrtLstPts(chkPts, range) # part points shortlisted in the hull range
            
#             if shtLstPts:
#                 return True
                

#             j = j+1
        
#         # print(np.max(cvxHull[0][0]))
#         return False

#      #Check if pts lie on left or right
#     def shrtLstPts (self, partPts, range):
#         i = 0
#         j = 0
#         unq = list()
#         ptsInRng = list()
#         while i < len(partPts):
#             [unq.append(x) for x in partPts[i] if partPts[i].all() not in unq]
#             i = i+1
        
#         unq = np.array_split(unq, len(unq)/2)
        
#         while j < len(unq):
#             if np.any(np.array(unq)[j][0]>=range[0])&np.any(np.array(unq)[j][0]<=range[1]):
#                 if np.any(np.array(unq)[j][1]>=range[2])&np.any(np.array(unq)[j][1]<=range[3]):
#                     ptsInRng.append(unq[j])
#             j = j +1

#         return(ptsInRng)

 

    