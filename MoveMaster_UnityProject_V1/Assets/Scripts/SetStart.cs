using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SetStart : MonoBehaviour
{
    public GameObject player;
    void Start() {
        player = GameObject.Find("Player");
    }
    private void OnMouseDown() {
        BlocksCopy bc_1 = player.GetComponent<BlocksCopy>();
        bc_1.SetSpawnCode_l();
        BlocksCopy_4 bc_2 = player.GetComponent<BlocksCopy_4>();
        bc_2.SetSpawnCode_r();
    }
}
