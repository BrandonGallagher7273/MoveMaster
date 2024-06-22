using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy : MonoBehaviour
{
    public GameObject prefab;
    public int blocks = 27;

    void Start()
    {
        int flag = 0;
        int count = 0;
        for (int i = 0; i < blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                GameObject clone = Instantiate(prefab);
                clone.transform.position = new Vector3(50+p*0.75f,.90f*count,50);
            }
            count++;
        }

    }

        /*
        int count = 0;
        for (int i = 0; i < 18; i++) {
            for(int a = 0; a < 3; a++) {
                GameObject clone = Instantiate(prefab);
                clone.transform.position = new Vector3(50,2,50+i*.75f);
            }
            count++;
        }
        */
 }


