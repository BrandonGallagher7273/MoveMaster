using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TowerReset : MonoBehaviour
{
    public GameObject player;
    public GameObject valid_checker;

    void Start() {
        player = GameObject.Find("Player");
        valid_checker = GameObject.Find("Valid_Check");
    }

    void OnMouseDown() {
        if (DestroyOnClick.started == false) {
            BlocksCopy bc_1 = player.GetComponent<BlocksCopy>();
            bc_1.ResetSpawnCode_l();
            BlocksCopy_4 bc_2 = player.GetComponent<BlocksCopy_4>();
            bc_2.ResetSpawnCode_r();
            DetectFall fall = valid_checker.GetComponent<DetectFall>();
            fall.ChangeMat(1);
        }
    }
}
